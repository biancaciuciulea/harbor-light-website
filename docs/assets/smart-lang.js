/**
 * Soft Soft Hour language suggestion on the author hub.
 * Priority: ?lang= → cookie → navigator.languages → optional geo → stay on hub.
 * Never hard-redirects. Never rewrites Amazon URLs.
 */
(function () {
  "use strict";

  var cfg = window.HARBOR_SMART_LANG || {};
  var supported = cfg.supported || ["en", "de", "fr", "es", "it"];
  var hubs = cfg.hubs || {
    en: "en.html",
    de: "de.html",
    fr: "fr.html",
    es: "es.html",
    it: "it.html",
  };
  var labels = cfg.labels || {
    en: "English",
    de: "Deutsch",
    fr: "Français",
    es: "Español",
    it: "Italiano",
  };
  var countryToLang = cfg.countryToLang || {};
  var useGeo = cfg.useGeo !== false;
  var basePath = cfg.basePath || "./";
  var cookiePref = "hl_soft_lang";
  var cookieDismiss = "hl_lang_banner";
  var cookieDays = 180;

  function readCookie(name) {
    var m = document.cookie.match(new RegExp("(?:^|; )" + name.replace(/[.*+?^${}()|[\]\\]/g, "\\$&") + "=([^;]*)"));
    return m ? decodeURIComponent(m[1]) : "";
  }

  function writeCookie(name, value, days) {
    var maxAge = Math.max(1, (days || cookieDays) * 86400);
    document.cookie =
      name +
      "=" +
      encodeURIComponent(value) +
      "; path=/; max-age=" +
      maxAge +
      "; SameSite=Lax";
  }

  function normalizeLang(code) {
    if (!code) return "";
    var raw = String(code).toLowerCase().replace("_", "-");
    var primary = raw.split("-")[0];
    return supported.indexOf(primary) >= 0 ? primary : "";
  }

  function hubUrl(lang) {
    var file = hubs[lang] || hubs.en || "en.html";
    return basePath + file;
  }

  function langFromQuery() {
    try {
      var q = new URLSearchParams(window.location.search).get("lang");
      return normalizeLang(q || "");
    } catch (e) {
      return "";
    }
  }

  function langFromNavigator() {
    var list = [];
    if (Array.isArray(navigator.languages)) list = navigator.languages.slice();
    else if (navigator.language) list = [navigator.language];
    for (var i = 0; i < list.length; i++) {
      var hit = normalizeLang(list[i]);
      if (hit) return hit;
    }
    return "";
  }

  function langFromCountry(country) {
    if (!country) return "";
    return normalizeLang(countryToLang[String(country).toUpperCase()] || "");
  }

  function setPref(lang) {
    var n = normalizeLang(lang);
    if (!n) return;
    writeCookie(cookiePref, n, cookieDays);
  }

  function dismissBanner() {
    writeCookie(cookieDismiss, "1", cookieDays);
    var el = document.getElementById("smart-lang-banner");
    if (el) {
      el.hidden = true;
      el.setAttribute("aria-hidden", "true");
    }
  }

  function showBanner(lang) {
    var el = document.getElementById("smart-lang-banner");
    if (!el || lang === "en") return;
    var label = labels[lang] || lang.toUpperCase();
    var msg = el.querySelector("[data-smart-lang-msg]");
    var go = el.querySelector("[data-smart-lang-go]");
    if (msg) {
      msg.textContent =
        "Free Soft Hour samples are available in " + label + " — Trailer + Chapter 1 + Chapter 2.";
    }
    if (go) {
      go.href = hubUrl(lang);
      go.textContent = "Continue in " + label;
      go.setAttribute("data-lang", lang);
    }
    el.hidden = false;
    el.removeAttribute("aria-hidden");
  }

  function wireManualLinks() {
    document.querySelectorAll("[data-smart-lang-set]").forEach(function (a) {
      a.addEventListener("click", function () {
        setPref(a.getAttribute("data-smart-lang-set") || "");
        writeCookie(cookieDismiss, "1", cookieDays);
      });
    });
    var go = document.querySelector("[data-smart-lang-go]");
    if (go) {
      go.addEventListener("click", function () {
        setPref(go.getAttribute("data-lang") || "");
        writeCookie(cookieDismiss, "1", cookieDays);
      });
    }
    var dismiss = document.querySelector("[data-smart-lang-dismiss]");
    if (dismiss) {
      dismiss.addEventListener("click", function () {
        setPref("en");
        dismissBanner();
      });
    }
  }

  function decideAndMaybeBanner(geoLang) {
    if (readCookie(cookieDismiss) === "1") return;

    var chosen =
      langFromQuery() ||
      normalizeLang(readCookie(cookiePref)) ||
      langFromNavigator() ||
      normalizeLang(geoLang || "") ||
      "en";

    if (langFromQuery()) {
      setPref(chosen);
      writeCookie(cookieDismiss, "1", cookieDays);
      if (chosen !== "en" && hubs[chosen]) {
        window.location.replace(hubUrl(chosen));
        return;
      }
    }

    if (chosen && chosen !== "en") {
      showBanner(chosen);
    }
  }

  function fetchGeoLang() {
    if (!useGeo || !window.fetch) return Promise.resolve("");
    var ctrl = typeof AbortController !== "undefined" ? new AbortController() : null;
    var timer = setTimeout(function () {
      if (ctrl) ctrl.abort();
    }, 1800);
    return fetch("https://get.geojs.io/v1/ip/country.json", {
      signal: ctrl ? ctrl.signal : undefined,
      credentials: "omit",
      cache: "no-store",
    })
      .then(function (r) {
        return r.ok ? r.json() : {};
      })
      .then(function (data) {
        return langFromCountry(data && (data.country || data.country_code));
      })
      .catch(function () {
        return "";
      })
      .finally(function () {
        clearTimeout(timer);
      });
  }

  function boot() {
    wireManualLinks();
    // Prefer browser language; only call geo if browser didn't match a Soft Hour lang.
    var navLang = langFromNavigator();
    if (navLang && navLang !== "en") {
      decideAndMaybeBanner("");
      return;
    }
    if (!useGeo) {
      decideAndMaybeBanner("");
      return;
    }
    fetchGeoLang().then(function (geoLang) {
      decideAndMaybeBanner(geoLang);
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
