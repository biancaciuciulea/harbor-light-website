/**
 * Harbor Light ARC — Google Apps Script Web App (FREE)
 * ----------------------------------------------------
 * Paste this file into script.google.com (Extensions → Apps Script on a Sheet,
 * or a standalone script). Deploy as Web App:
 *   Execute as: Me
 *   Who has access: Anyone
 *
 * Then paste the /exec URL into harbor-light-website/config.py → ARC_FORM_ENDPOINT
 * and run: python generator.py && git push
 *
 * What it does on each ARC signup POST:
 *   1. Append a row to the linked Google Sheet (auto registry)
 *   2. Email the reader (localized EN/DE/FR/ES/IT) with EPUB + Send to Kindle + review
 *   3. Email the owner (Script Property OWNER_EMAIL, default below)
 *   4. Return JSON { ok: true } for the site AJAX thank-you panel
 *
 * Script Properties (optional, File → Project properties → Script properties):
 *   OWNER_EMAIL   — default: ing.biancaciuciulea@yahoo.com
 *   SHEET_NAME    — default: ARC Signups
 *   SITE_BASE     — default: https://picubiancamaria.com
 *
 * Bound to a Spreadsheet: uses that spreadsheet automatically.
 * Standalone: creates "Harbor Light ARC Signups" on first run (or set SHEET_ID).
 */

var DEFAULT_OWNER = "ing.biancaciuciulea@yahoo.com";
var DEFAULT_SHEET_NAME = "ARC Signups";
var DEFAULT_SITE_BASE = "https://picubiancamaria.com";

var HEADERS = [
  "timestamp",
  "email",
  "first_name",
  "lang",
  "book_id",
  "book_title",
  "asin",
  "review_url",
  "epub_url",
  "sendtokindle_url",
  "delivery_format",
  "age_18",
  "honest_review",
  "utm_source",
  "utm_medium",
  "utm_campaign",
  "utm_content",
  "form_type",
  "subject",
];

/** Localized reader email copy (page language). */
var EMAIL_I18N = {
  en: {
    subject: "Your Harbor Light ARC — download link inside",
    greeting: "Hi",
    greeting_anon: "Hi there",
    thanks:
      "Thank you for joining the Harbor Light ARC Team. Your free EPUB is ready.",
    download: "Download EPUB",
    kindle: "Send to Kindle",
    review: "Leave an honest Amazon review (after you finish)",
    note:
      "Stars are not for sale. DNF is fine — just do not fake a finish. You can also grab the file from the thank-you panel on the site.",
    sign: "Warmly,\nPicu Bianca-Maria\nhttps://picubiancamaria.com/arc.html",
  },
  de: {
    subject: "Dein Harbor Light ARC — Download-Link innen",
    greeting: "Hallo",
    greeting_anon: "Hallo",
    thanks:
      "Danke, dass du dem Harbor Light ARC-Team beitrittst. Dein kostenloses EPUB ist bereit.",
    download: "EPUB herunterladen",
    kindle: "An Kindle senden",
    review: "Ehrliche Amazon-Rezension hinterlassen (nach dem Lesen)",
    note:
      "Sterne sind nicht käuflich. DNF ist in Ordnung — bitte keinen Abschluss vortäuschen. Den Link findest du auch auf der Danke-Seite.",
    sign: "Herzliche Grüße,\nPicu Bianca-Maria\nhttps://picubiancamaria.com/de/arc.html",
  },
  fr: {
    subject: "Votre ARC Harbor Light — lien de téléchargement",
    greeting: "Bonjour",
    greeting_anon: "Bonjour",
    thanks:
      "Merci de rejoindre l’équipe ARC Harbor Light. Votre EPUB gratuit est prêt.",
    download: "Télécharger l’EPUB",
    kindle: "Envoyer vers Kindle",
    review: "Laisser un avis Amazon honnête (après lecture)",
    note:
      "Les étoiles ne s’achètent pas. Un DNF est OK — ne simulez pas une fin. Le lien est aussi sur la page de confirmation.",
    sign: "Bien à vous,\nPicu Bianca-Maria\nhttps://picubiancamaria.com/fr/arc.html",
  },
  es: {
    subject: "Tu ARC de Harbor Light — enlace de descarga",
    greeting: "Hola",
    greeting_anon: "Hola",
    thanks:
      "Gracias por unirte al equipo ARC de Harbor Light. Tu EPUB gratis está listo.",
    download: "Descargar EPUB",
    kindle: "Enviar a Kindle",
    review: "Dejar una reseña honesta en Amazon (cuando termines)",
    note:
      "Las estrellas no se compran. DNF está bien — no finjas haber terminado. El enlace también está en la página de gracias.",
    sign: "Un abrazo,\nPicu Bianca-Maria\nhttps://picubiancamaria.com/es/arc.html",
  },
  it: {
    subject: "Il tuo ARC Harbor Light — link per scaricare",
    greeting: "Ciao",
    greeting_anon: "Ciao",
    thanks:
      "Grazie per esserti unito/a al team ARC Harbor Light. Il tuo EPUB gratuito è pronto.",
    download: "Scarica EPUB",
    kindle: "Invia a Kindle",
    review: "Lascia una recensione onesta su Amazon (quando finisci)",
    note:
      "Le stelle non si comprano. Il DNF va bene — non fingere di aver finito. Il link è anche nella pagina di ringraziamento.",
    sign: "A presto,\nPicu Bianca-Maria\nhttps://picubiancamaria.com/it/arc.html",
  },
};

var SENDTOKINDLE = {
  en: "https://www.amazon.com/sendtokindle",
  de: "https://www.amazon.de/sendtokindle",
  fr: "https://www.amazon.fr/sendtokindle",
  es: "https://www.amazon.es/sendtokindle",
  it: "https://www.amazon.it/sendtokindle",
};

function doGet() {
  return jsonOut_({
    ok: true,
    service: "harbor-light-arc",
    hint: "POST form fields: email, first_name, lang, book_id, asin, review_url, epub_url, …",
  });
}

function doPost(e) {
  try {
    var data = parsePost_(e);
    // Honeypot — pretend success, do nothing
    if (String(data._gotcha || data.gotcha || "").trim()) {
      return jsonOut_({ ok: true, skipped: "honeypot" });
    }

    var email = String(data.email || "").trim();
    if (!email || email.indexOf("@") < 1) {
      return jsonOut_({ ok: false, error: "email required" }, 400);
    }

    var lang = normalizeLang_(data.lang);
    var firstName = String(data.first_name || data.name || "").trim();
    var bookId = String(data.book_id || data.book || "").trim();
    var bookTitle = String(data.book_title || "").trim();
    var asin = String(data.asin || "").trim();
    var reviewUrl = String(data.review_url || "").trim();
    var epubUrl = String(data.epub_url || "").trim();
    var sendtokindle =
      String(data.sendtokindle_url || "").trim() || SENDTOKINDLE[lang] || SENDTOKINDLE.en;
    var delivery = String(data.delivery_format || "epub").trim() || "epub";
    var age18 = String(data.age_18 || "").trim();
    var honest = String(data.honest_review || "").trim();
    var formType = String(data.form_type || "arc").trim() || "arc";
    var subject = String(data._subject || data.subject || "").trim();
    var utm = {
      source: String(data.utm_source || "").trim(),
      medium: String(data.utm_medium || "").trim(),
      campaign: String(data.utm_campaign || "").trim(),
      content: String(data.utm_content || "").trim(),
    };

    appendSignupRow_({
      email: email,
      first_name: firstName,
      lang: lang,
      book_id: bookId,
      book_title: bookTitle,
      asin: asin,
      review_url: reviewUrl,
      epub_url: epubUrl,
      sendtokindle_url: sendtokindle,
      delivery_format: delivery,
      age_18: age18,
      honest_review: honest,
      utm_source: utm.source,
      utm_medium: utm.medium,
      utm_campaign: utm.campaign,
      utm_content: utm.content,
      form_type: formType,
      subject: subject,
    });

    if (epubUrl) {
      sendReaderEmail_({
        to: email,
        first_name: firstName,
        lang: lang,
        book_title: bookTitle,
        book_id: bookId,
        epub_url: epubUrl,
        sendtokindle_url: sendtokindle,
        review_url: reviewUrl,
        asin: asin,
      });
    }

    sendOwnerEmail_({
      email: email,
      first_name: firstName,
      lang: lang,
      book_id: bookId,
      book_title: bookTitle,
      asin: asin,
      review_url: reviewUrl,
      epub_url: epubUrl,
      utm: utm,
    });

    return jsonOut_({ ok: true });
  } catch (err) {
    return jsonOut_({ ok: false, error: String(err && err.message ? err.message : err) }, 500);
  }
}

function parsePost_(e) {
  var out = {};
  if (!e) return out;
  if (e.parameter) {
    Object.keys(e.parameter).forEach(function (k) {
      out[k] = e.parameter[k];
    });
  }
  if (e.postData && e.postData.contents) {
    var raw = e.postData.contents;
    var type = String((e.postData.type || "")).toLowerCase();
    if (type.indexOf("application/json") >= 0) {
      try {
        var parsed = JSON.parse(raw);
        Object.keys(parsed).forEach(function (k) {
          out[k] = parsed[k];
        });
      } catch (ignore) {
        /* keep parameter map */
      }
    }
  }
  return out;
}

function normalizeLang_(raw) {
  var code = String(raw || "en").toLowerCase().slice(0, 2);
  if (EMAIL_I18N[code]) return code;
  return "en";
}

function prop_(key, fallback) {
  var v = PropertiesService.getScriptProperties().getProperty(key);
  return v && String(v).trim() ? String(v).trim() : fallback;
}

function getSheet_() {
  var name = prop_("SHEET_NAME", DEFAULT_SHEET_NAME);
  var ss = null;
  try {
    ss = SpreadsheetApp.getActiveSpreadsheet();
  } catch (ignore) {
    ss = null;
  }
  if (!ss) {
    var sheetId = prop_("SHEET_ID", "");
    if (sheetId) {
      ss = SpreadsheetApp.openById(sheetId);
    } else {
      ss = SpreadsheetApp.create("Harbor Light ARC Signups");
      PropertiesService.getScriptProperties().setProperty("SHEET_ID", ss.getId());
    }
  }
  var sh = ss.getSheetByName(name);
  if (!sh) sh = ss.insertSheet(name);
  ensureHeaders_(sh);
  return sh;
}

function ensureHeaders_(sh) {
  var lastCol = Math.max(sh.getLastColumn(), HEADERS.length);
  var existing = sh.getRange(1, 1, 1, HEADERS.length).getValues()[0];
  var blank = !existing || !existing[0];
  if (blank) {
    sh.getRange(1, 1, 1, HEADERS.length).setValues([HEADERS]);
    sh.setFrozenRows(1);
  }
}

function appendSignupRow_(row) {
  var sh = getSheet_();
  sh.appendRow([
    new Date().toISOString(),
    row.email,
    row.first_name,
    row.lang,
    row.book_id,
    row.book_title,
    row.asin,
    row.review_url,
    row.epub_url,
    row.sendtokindle_url,
    row.delivery_format,
    row.age_18,
    row.honest_review,
    row.utm_source,
    row.utm_medium,
    row.utm_campaign,
    row.utm_content,
    row.form_type,
    row.subject,
  ]);
}

function sendReaderEmail_(opts) {
  var t = EMAIL_I18N[opts.lang] || EMAIL_I18N.en;
  var name = opts.first_name;
  var hello = name ? t.greeting + " " + name + "," : t.greeting_anon + ",";
  var titleBit = opts.book_title
    ? opts.book_title
    : opts.book_id
      ? "Book " + opts.book_id
      : "Harbor Light";
  var lines = [
    hello,
    "",
    t.thanks,
    "",
    titleBit,
    "",
    t.download + ":",
    opts.epub_url,
    "",
    t.kindle + ":",
    opts.sendtokindle_url,
  ];
  if (opts.review_url) {
    lines.push("", t.review + ":", opts.review_url);
  } else if (opts.asin) {
    lines.push(
      "",
      t.review + ":",
      "https://www.amazon.com/review/create-review?asin=" + opts.asin
    );
  }
  lines.push("", t.note, "", t.sign);
  MailApp.sendEmail({
    to: opts.to,
    subject: t.subject,
    body: lines.join("\n"),
    name: "Picu Bianca-Maria",
  });
}

function sendOwnerEmail_(opts) {
  var owner = prop_("OWNER_EMAIL", DEFAULT_OWNER);
  if (!owner) return;
  var utm = opts.utm || {};
  var body = [
    "New ARC signup",
    "",
    "Email: " + opts.email,
    "Name: " + (opts.first_name || "—"),
    "Lang: " + opts.lang,
    "Book: " + (opts.book_id || "—") + (opts.book_title ? " — " + opts.book_title : ""),
    "ASIN: " + (opts.asin || "—"),
    "EPUB: " + (opts.epub_url || "—"),
    "Review: " + (opts.review_url || "—"),
    "UTM: " +
      [utm.source, utm.medium, utm.campaign, utm.content].filter(Boolean).join(" / "),
    "",
    "Sheet row appended. Reader email " +
      (opts.epub_url ? "sent." : "skipped (no epub_url)."),
  ].join("\n");
  MailApp.sendEmail({
    to: owner,
    subject:
      "[ARC] " +
      (opts.lang || "en").toUpperCase() +
      " book" +
      (opts.book_id || "?") +
      " — " +
      opts.email,
    body: body,
    name: "Harbor Light ARC",
  });
}

function jsonOut_(obj, _statusIgnored) {
  // Apps Script ContentService cannot set HTTP status reliably for web apps;
  // clients treat res.ok + {ok:true/false}.
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(
    ContentService.MimeType.JSON
  );
}
