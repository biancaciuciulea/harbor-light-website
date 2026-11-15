(function () {
  "use strict";

  function bindToggle(btn) {
    var navId = btn.getAttribute("aria-controls");
    var nav = navId ? document.getElementById(navId) : null;
    if (!nav) return;

    function setOpen(open) {
      btn.setAttribute("aria-expanded", open ? "true" : "false");
      btn.setAttribute("aria-label", open ? "Close menu" : "Open menu");
      nav.classList.toggle("is-open", open);
      document.body.classList.toggle("nav-open", open);
      if (!open) {
        nav.querySelectorAll("details.nav-lang[open]").forEach(function (d) {
          d.open = false;
        });
      }
    }

    btn.addEventListener("click", function () {
      setOpen(btn.getAttribute("aria-expanded") !== "true");
    });

    nav.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () {
        setOpen(false);
      });
    });

    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape") setOpen(false);
    });

    window.addEventListener("resize", function () {
      if (window.matchMedia("(min-width: 901px)").matches) setOpen(false);
    });
  }

  function bindLangMenus() {
    document.querySelectorAll("details.nav-lang").forEach(function (details) {
      document.addEventListener("click", function (event) {
        if (!details.open) return;
        if (details.contains(event.target)) return;
        details.open = false;
      });
    });
  }

  document.querySelectorAll(".nav-toggle").forEach(bindToggle);
  bindLangMenus();
})();
