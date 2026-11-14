/**
 * Soft Hour conversion events for GA4 (via gtag).
 * Fires: soft_hour_cta (+ recommended GA4 events where useful).
 */
(function () {
  "use strict";

  function send(name, params) {
    if (typeof window.gtag !== "function") return;
    window.gtag("event", name, params || {});
  }

  function classify(anchor) {
    var explicit = (anchor.getAttribute("data-ga-cta") || "").trim();
    if (explicit) {
      return {
        cta_id: explicit,
        cta_label: (anchor.getAttribute("data-ga-label") || anchor.textContent || explicit)
          .replace(/\s+/g, " ")
          .trim()
          .slice(0, 100),
        destination: (anchor.getAttribute("data-ga-dest") || "").trim() || explicit,
      };
    }

    var href = anchor.href || "";
    var host = "";
    var path = "";
    try {
      var u = new URL(href, window.location.href);
      host = u.hostname.replace(/^www\./, "");
      path = u.pathname || "";
    } catch (err) {
      return null;
    }

    var label = (anchor.textContent || "").replace(/\s+/g, " ").trim().slice(0, 100);

    if (host.indexOf("gumroad.com") !== -1) {
      return { cta_id: "gumroad_soft_hour", cta_label: label || "Gumroad Soft Hour", destination: "gumroad" };
    }
    if (host.indexOf("open.spotify.com") !== -1 || host.indexOf("spotify.com") !== -1) {
      return { cta_id: "spotify_sample", cta_label: label || "Spotify sample", destination: "spotify" };
    }
    if (host.indexOf("amazon.") !== -1 && /\/dp\//.test(path)) {
      return { cta_id: "kindle_ebook", cta_label: label || "Kindle ebook", destination: "amazon" };
    }
    if (host.indexOf("goodreads.com") !== -1) {
      return { cta_id: "goodreads", cta_label: label || "Goodreads", destination: "goodreads" };
    }
    if (host.indexOf("youtube.com") !== -1 || host.indexOf("youtu.be") !== -1) {
      return { cta_id: "youtube_ro", cta_label: label || "YouTube", destination: "youtube" };
    }
    if (/harbor-light\.html$/i.test(path) || /\/harbor-light\.html$/i.test(path)) {
      return { cta_id: "series_hub", cta_label: label || "Harbor Light series", destination: "series_hub" };
    }
    if (/harbor-light-sample-chapter/i.test(path)) {
      return { cta_id: "sample_chapter", cta_label: label || "Sample chapter", destination: "sample" };
    }
    if (/harbor-light-audiobook-guide/i.test(path)) {
      return { cta_id: "soft_hour_guide", cta_label: label || "Soft Hour guide", destination: "guide" };
    }
    return null;
  }

  function trackAnchor(anchor) {
    var info = classify(anchor);
    if (!info) return;

    var params = {
      cta_id: info.cta_id,
      cta_label: info.cta_label,
      destination: info.destination,
      link_url: anchor.href,
      page_path: window.location.pathname,
    };

    send("soft_hour_cta", params);

    if (info.destination === "gumroad") {
      send("select_content", { content_type: "soft_hour_audiobook", item_id: info.cta_id });
    } else if (info.destination === "spotify") {
      send("select_content", { content_type: "spotify_sample", item_id: info.cta_id });
    } else if (info.destination === "series_hub") {
      send("select_content", { content_type: "series_hub", item_id: info.cta_id });
    } else if (info.destination === "amazon") {
      send("select_content", { content_type: "kindle_ebook", item_id: info.cta_id });
    }
  }

  document.addEventListener(
    "click",
    function (event) {
      var anchor = event.target && event.target.closest ? event.target.closest("a[href]") : null;
      if (!anchor) return;
      trackAnchor(anchor);
    },
    true
  );

  document.addEventListener(
    "submit",
    function (event) {
      var form = event.target;
      if (!form || form.tagName !== "FORM") return;
      var action = (form.getAttribute("action") || "").toLowerCase();
      if (action.indexOf("formspree.io") === -1) return;
      send("generate_lead", {
        method: "formspree",
        page_path: window.location.pathname,
      });
      send("soft_hour_cta", {
        cta_id: "email_signup",
        cta_label: "Email signup",
        destination: "formspree",
        page_path: window.location.pathname,
      });
    },
    true
  );
})();
