# -*- coding: utf-8 -*-
"""Pull a weekly GA4 summary via the Analytics Data API.

Setup (one-time):
  1. Google Cloud → create/select a project → enable "Google Analytics Data API"
  2. IAM → Service Accounts → Create → download JSON key → save as secrets/ga4-service-account.json
  3. GA4 Admin → Property access management → Add the service-account email as Viewer
  4. GA4 Admin → Property settings → copy numeric Property ID (not G-XXXXXXXX)
  5. Copy .env.example → .env and fill GA4_PROPERTY_ID (+ optional SMTP for email)

Run:
  python scripts/ga4_weekly_report.py
  python scripts/ga4_weekly_report.py --days 7 --email
"""

from __future__ import annotations

import argparse
import os
import smtplib
import ssl
from datetime import datetime, timezone
from email.message import EmailMessage
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORTS_DIR = ROOT / "reports"
DEFAULT_CREDS = ROOT / "secrets" / "ga4-service-account.json"


def _load_dotenv(path: Path) -> None:
    """Load KEY=VALUE pairs from .env into os.environ (no extra dependency)."""
    if not path.is_file():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, val = line.partition("=")
        key = key.strip()
        val = val.strip().strip('"').strip("'")
        os.environ.setdefault(key, val)


def _client(creds_path: Path):
    from google.analytics.data_v1beta import BetaAnalyticsDataClient

    if not creds_path.is_file():
        raise FileNotFoundError(
            f"Missing credentials: {creds_path}\n"
            "Download a service-account JSON key and place it there."
        )
    return BetaAnalyticsDataClient.from_service_account_json(str(creds_path))


def _run(client, property_id: str, dimensions: list[str], metrics: list[str], days: int, limit: int = 10):
    from google.analytics.data_v1beta.types import (
        DateRange,
        Dimension,
        Metric,
        OrderBy,
        RunReportRequest,
    )

    request = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[Dimension(name=d) for d in dimensions],
        metrics=[Metric(name=m) for m in metrics],
        date_ranges=[DateRange(start_date=f"{days}daysAgo", end_date="yesterday")],
        limit=limit,
        order_bys=[
            OrderBy(metric=OrderBy.MetricOrderBy(metric_name=metrics[0]), desc=True)
        ]
        if metrics
        else None,
    )
    return client.run_report(request)


def _rows(response) -> list[tuple[list[str], list[str]]]:
    out: list[tuple[list[str], list[str]]] = []
    for row in response.rows:
        dims = [d.value for d in row.dimension_values]
        mets = [m.value for m in row.metric_values]
        out.append((dims, mets))
    return out


def build_report(property_id: str, creds_path: Path, days: int) -> str:
    client = _client(creds_path)

    overview = _run(
        client,
        property_id,
        dimensions=[],
        metrics=["sessions", "totalUsers", "screenPageViews", "bounceRate", "averageSessionDuration"],
        days=days,
        limit=1,
    )
    ov = _rows(overview)
    sessions = users = views = bounce = duration = "0"
    if ov:
        sessions, users, views, bounce, duration = ov[0][1]

    pages = _rows(
        _run(
            client,
            property_id,
            dimensions=["pagePath"],
            metrics=["screenPageViews", "totalUsers"],
            days=days,
            limit=10,
        )
    )
    sources = _rows(
        _run(
            client,
            property_id,
            dimensions=["sessionDefaultChannelGroup"],
            metrics=["sessions", "totalUsers"],
            days=days,
            limit=8,
        )
    )
    countries = _rows(
        _run(
            client,
            property_id,
            dimensions=["country"],
            metrics=["totalUsers", "sessions"],
            days=days,
            limit=8,
        )
    )
    events = _rows(
        _run(
            client,
            property_id,
            dimensions=["eventName"],
            metrics=["eventCount", "totalUsers"],
            days=days,
            limit=15,
        )
    )
    soft_hour: list[tuple[list[str], list[str]]] = []
    try:
        soft_hour = _rows(
            _run(
                client,
                property_id,
                dimensions=["customEvent:cta_id"],
                metrics=["eventCount", "totalUsers"],
                days=days,
                limit=12,
            )
        )
    except Exception:
        # cta_id must be registered as an event-scoped custom dimension in GA4 Admin
        soft_hour = []

    try:
        bounce_pct = f"{float(bounce) * 100:.1f}%"
    except ValueError:
        bounce_pct = bounce
    try:
        dur_s = float(duration)
        duration_fmt = f"{int(dur_s // 60)}m {int(dur_s % 60)}s"
    except ValueError:
        duration_fmt = duration

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        f"# GA4 weekly report — picubiancamaria.com",
        "",
        f"- Generated: {now}",
        f"- Range: last {days} days (through yesterday)",
        f"- Property: `{property_id}`",
        "",
        "## Overview",
        f"- Sessions: **{sessions}**",
        f"- Users: **{users}**",
        f"- Page views: **{views}**",
        f"- Bounce rate: **{bounce_pct}**",
        f"- Avg. session: **{duration_fmt}**",
        "",
        "## Top pages",
    ]
    if not pages:
        lines.append("_No page data yet (wait until GA4 has traffic)._")
    else:
        for dims, mets in pages:
            lines.append(f"- `{dims[0]}` — {mets[0]} views · {mets[1]} users")

    lines += ["", "## Channels"]
    if not sources:
        lines.append("_No channel data yet._")
    else:
        for dims, mets in sources:
            lines.append(f"- {dims[0]} — {mets[0]} sessions · {mets[1]} users")

    lines += ["", "## Countries"]
    if not countries:
        lines.append("_No country data yet._")
    else:
        for dims, mets in countries:
            lines.append(f"- {dims[0]} — {mets[0]} users · {mets[1]} sessions")

    lines += ["", "## Events"]
    if not events:
        lines.append("_No event data yet._")
    else:
        for dims, mets in events:
            lines.append(f"- `{dims[0]}` — {mets[0]} events · {mets[1]} users")

    lines += ["", "## Soft Hour CTA (`cta_id`)"]
    if not soft_hour:
        lines.append(
            "_No `soft_hour_cta` / `cta_id` data yet — wait 24–48h after deploy, "
            "or register `cta_id` as an event-scoped custom dimension in GA4 Admin._"
        )
    else:
        for dims, mets in soft_hour:
            lines.append(f"- `{dims[0]}` — {mets[0]} events · {mets[1]} users")

    lines.append("")
    return "\n".join(lines)


def send_email(body: str, days: int) -> None:
    host = os.environ.get("SMTP_HOST", "").strip()
    port = int(os.environ.get("SMTP_PORT", "587"))
    user = os.environ.get("SMTP_USER", "").strip()
    password = os.environ.get("SMTP_PASSWORD", "").strip()
    mail_from = os.environ.get("REPORT_FROM", user).strip()
    mail_to = os.environ.get("REPORT_TO", "").strip()

    if not all([host, user, password, mail_to]):
        raise SystemExit(
            "Email requested but SMTP incomplete. Set SMTP_HOST, SMTP_USER, "
            "SMTP_PASSWORD, REPORT_TO in .env"
        )

    msg = EmailMessage()
    msg["Subject"] = f"picubiancamaria.com — GA4 last {days} days"
    msg["From"] = mail_from
    msg["To"] = mail_to
    msg.set_content(body)

    context = ssl.create_default_context()
    with smtplib.SMTP(host, port, timeout=30) as smtp:
        smtp.starttls(context=context)
        smtp.login(user, password)
        smtp.send_message(msg)
    print(f"Emailed report to {mail_to}")


def main() -> None:
    _load_dotenv(ROOT / ".env")

    parser = argparse.ArgumentParser(description="GA4 weekly report via Data API")
    parser.add_argument("--days", type=int, default=int(os.environ.get("GA4_REPORT_DAYS", "7")))
    parser.add_argument(
        "--property-id",
        default=os.environ.get("GA4_PROPERTY_ID", "").strip(),
        help="Numeric GA4 property ID (Admin → Property settings)",
    )
    parser.add_argument(
        "--credentials",
        type=Path,
        default=Path(os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", str(DEFAULT_CREDS))),
    )
    parser.add_argument("--email", action="store_true", help="Also send via SMTP from .env")
    parser.add_argument("--print-only", action="store_true", help="Do not write reports/")
    args = parser.parse_args()

    if not args.property_id or args.property_id.startswith("YOUR"):
        raise SystemExit(
            "Set GA4_PROPERTY_ID in .env (Admin → Property settings → Property ID).\n"
            "This is a number like 123456789 — not G-6TC0BTZ83E."
        )

    md = build_report(args.property_id, args.credentials.expanduser(), args.days)
    print(md)

    if not args.print_only:
        REPORTS_DIR.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now(timezone.utc).strftime("%Y%m%d")
        latest = REPORTS_DIR / "ga4-latest.md"
        archived = REPORTS_DIR / f"ga4-{stamp}.md"
        latest.write_text(md, encoding="utf-8")
        archived.write_text(md, encoding="utf-8")
        print(f"\nWrote {latest.relative_to(ROOT)} and {archived.relative_to(ROOT)}")

    if args.email:
        send_email(md, args.days)


if __name__ == "__main__":
    main()
