/* Osama Altaf — site interactions: theme, mobile menu, scrollspy, copy buttons */
(function () {
  "use strict";

  /* ---------- theme ---------- */
  var root = document.documentElement;
  var stored = null;
  try { stored = localStorage.getItem("theme"); } catch (e) {}
  // Default to LIGHT for all visitors; only honor an explicit user choice.
  root.setAttribute("data-theme", stored === "dark" ? "dark" : "light");
  var toggle = document.getElementById("themeToggle");
  if (toggle) {
    toggle.addEventListener("click", function () {
      var next = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
      root.setAttribute("data-theme", next);
      try { localStorage.setItem("theme", next); } catch (e) {}
    });
  }

  /* ---------- mobile menu ---------- */
  var menuBtn = document.getElementById("menuBtn");
  var links = document.querySelector(".nav-links");
  if (menuBtn && links) {
    menuBtn.addEventListener("click", function () {
      var open = links.classList.toggle("open");
      menuBtn.setAttribute("aria-expanded", open ? "true" : "false");
    });
    links.addEventListener("click", function (e) {
      if (e.target.tagName === "A") {
        links.classList.remove("open");
        menuBtn.setAttribute("aria-expanded", "false");
      }
    });
  }

  /* ---------- scrollspy ---------- */
  var navAnchors = Array.prototype.slice.call(document.querySelectorAll(".nav-links a[href^='#']"));
  if (navAnchors.length && "IntersectionObserver" in window) {
    var map = {};
    navAnchors.forEach(function (a) {
      var id = a.getAttribute("href").slice(1);
      var sec = document.getElementById(id);
      if (sec) map[id] = a;
    });
    var obs = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          navAnchors.forEach(function (a) { a.classList.remove("active"); });
          var active = map[en.target.id];
          if (active) active.classList.add("active");
        }
      });
    }, { rootMargin: "-45% 0px -50% 0px", threshold: 0 });
    Object.keys(map).forEach(function (id) {
      var sec = document.getElementById(id);
      if (sec) obs.observe(sec);
    });
  }

  /* ---------- year ---------- */
  var y = document.getElementById("year");
  if (y) y.textContent = new Date().getFullYear();

  /* ---------- toast ---------- */
  var toastEl = null, toastTimer = null;
  function toast(msg) {
    if (!toastEl) {
      toastEl = document.createElement("div");
      toastEl.className = "toast";
      document.body.appendChild(toastEl);
    }
    toastEl.textContent = msg;
    toastEl.classList.add("show");
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () { toastEl.classList.remove("show"); }, 1900);
  }

  function copyText(text, label) {
    function done() { toast((label || "Copied") + " ✓"); }
    function fallback() {
      var ta = document.createElement("textarea");
      ta.value = text; ta.style.position = "fixed"; ta.style.opacity = "0";
      document.body.appendChild(ta); ta.select();
      try { document.execCommand("copy"); done(); } catch (e) { toast("Copy failed"); }
      document.body.removeChild(ta);
    }
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(done).catch(fallback);
    } else { fallback(); }
  }

  /* ---------- copy buttons ----------
     data-copy="literal text"  OR  data-copy-link="/path" (resolved to absolute URL) */
  document.addEventListener("click", function (e) {
    var btn = e.target.closest ? e.target.closest("[data-copy],[data-copy-link]") : null;
    if (!btn) return;
    e.preventDefault();
    if (btn.hasAttribute("data-copy-link")) {
      var url = new URL(btn.getAttribute("data-copy-link"), window.location.origin).href;
      copyText(url, btn.getAttribute("data-copy-label") || "Link copied");
    } else {
      copyText(btn.getAttribute("data-copy"), btn.getAttribute("data-copy-label") || "Copied");
    }
  });

  /* ---------- fill share links on hub with the live origin ---------- */
  Array.prototype.slice.call(document.querySelectorAll("[data-show-url]")).forEach(function (el) {
    var path = el.getAttribute("data-show-url");
    el.textContent = window.location.host + path;
  });
})();
