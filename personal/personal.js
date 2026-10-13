/* /personal: interactions. Vanilla JS, no dependencies. */
(function () {
  "use strict";

  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var finePointer = window.matchMedia("(pointer: fine)").matches;

  /* ---------- year ---------- */
  var y = document.getElementById("year");
  if (y) y.textContent = new Date().getFullYear();

  /* ---------- hero neural field ---------- */
  var canvas = document.getElementById("field");
  if (canvas && canvas.getContext) {
    var ctx = canvas.getContext("2d");
    var dpr = Math.min(window.devicePixelRatio || 1, 2);
    var W = 0, H = 0, nodes = [], pulses = [], mouse = { x: -9999, y: -9999 };
    var running = true, raf = 0;
    var COLORS = ["124,156,255", "179,139,255", "93,226,214"];

    function resize() {
      var r = canvas.getBoundingClientRect();
      W = r.width; H = r.height;
      canvas.width = Math.round(W * dpr); canvas.height = Math.round(H * dpr);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      var count = Math.round(Math.min(110, Math.max(40, (W * H) / 16000)));
      nodes = [];
      for (var i = 0; i < count; i++) {
        nodes.push({
          x: Math.random() * W, y: Math.random() * H,
          vx: (Math.random() - 0.5) * 0.25, vy: (Math.random() - 0.5) * 0.25,
          r: Math.random() * 1.6 + 0.6, c: COLORS[i % 3]
        });
      }
      pulses = [];
    }

    var LINK = 140;
    function step() {
      ctx.clearRect(0, 0, W, H);
      var i, j, a, b, dx, dy, d;
      for (i = 0; i < nodes.length; i++) {
        a = nodes[i];
        if (!reduce) {
          a.x += a.vx; a.y += a.vy;
          if (a.x < -20) a.x = W + 20; else if (a.x > W + 20) a.x = -20;
          if (a.y < -20) a.y = H + 20; else if (a.y > H + 20) a.y = -20;
          dx = mouse.x - a.x; dy = mouse.y - a.y; d = dx * dx + dy * dy;
          if (d < 32000) { a.x -= dx * 0.004; a.y -= dy * 0.004; }
        }
      }
      for (i = 0; i < nodes.length; i++) {
        a = nodes[i];
        for (j = i + 1; j < nodes.length; j++) {
          b = nodes[j];
          dx = a.x - b.x; dy = a.y - b.y; d = Math.sqrt(dx * dx + dy * dy);
          if (d < LINK) {
            var near = Math.max(0, 1 - (Math.hypot(mouse.x - a.x, mouse.y - a.y) / 260));
            ctx.strokeStyle = "rgba(" + a.c + "," + ((1 - d / LINK) * (0.22 + near * 0.5)).toFixed(3) + ")";
            ctx.lineWidth = 1;
            ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y); ctx.stroke();
            if (!reduce && pulses.length < 14 && Math.random() < 0.0009) pulses.push({ a: a, b: b, t: 0, c: a.c });
          }
        }
      }
      for (i = 0; i < nodes.length; i++) {
        a = nodes[i];
        ctx.fillStyle = "rgba(" + a.c + ",.85)";
        ctx.beginPath(); ctx.arc(a.x, a.y, a.r, 0, 6.283); ctx.fill();
      }
      for (i = pulses.length - 1; i >= 0; i--) {
        var p = pulses[i];
        p.t += 0.018;
        if (p.t >= 1) { pulses.splice(i, 1); continue; }
        var px = p.a.x + (p.b.x - p.a.x) * p.t, py = p.a.y + (p.b.y - p.a.y) * p.t;
        var g = ctx.createRadialGradient(px, py, 0, px, py, 10);
        g.addColorStop(0, "rgba(" + p.c + ",.95)"); g.addColorStop(1, "rgba(" + p.c + ",0)");
        ctx.fillStyle = g; ctx.beginPath(); ctx.arc(px, py, 10, 0, 6.283); ctx.fill();
      }
      if (running && !reduce) raf = requestAnimationFrame(step);
    }

    resize(); step();
    var rt;
    window.addEventListener("resize", function () { clearTimeout(rt); rt = setTimeout(function () { resize(); if (reduce) step(); }, 150); });
    canvas.parentElement.addEventListener("pointermove", function (e) {
      var r = canvas.getBoundingClientRect(); mouse.x = e.clientX - r.left; mouse.y = e.clientY - r.top;
    });
    canvas.parentElement.addEventListener("pointerleave", function () { mouse.x = mouse.y = -9999; });
    if ("IntersectionObserver" in window) {
      new IntersectionObserver(function (en) {
        var vis = en[0].isIntersecting;
        if (vis && !running) { running = true; if (!reduce) raf = requestAnimationFrame(step); }
        else if (!vis) { running = false; cancelAnimationFrame(raf); }
      }).observe(canvas);
    }
    document.addEventListener("visibilitychange", function () {
      if (document.hidden) { running = false; cancelAnimationFrame(raf); }
      else if (!running) { running = true; if (!reduce) raf = requestAnimationFrame(step); }
    });
  }

  /* ---------- reveal on scroll (with sibling stagger) ---------- */
  var rv = Array.prototype.slice.call(document.querySelectorAll(".rv"));
  rv.forEach(function (el) {
    var sibs = Array.prototype.filter.call(el.parentElement.children, function (c) { return c.classList.contains("rv"); });
    var idx = sibs.indexOf(el);
    if (idx > 0) el.style.setProperty("--rd", Math.min(idx, 6) * 0.08 + "s");
  });
  if ("IntersectionObserver" in window && !reduce) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    rv.forEach(function (el) { io.observe(el); });
  } else {
    rv.forEach(function (el) { el.classList.add("in"); });
  }

  /* ---------- count-up stats ---------- */
  function countUp(el) {
    var to = parseFloat(el.getAttribute("data-count"));
    var dec = parseInt(el.getAttribute("data-dec") || "0", 10);
    var pre = el.getAttribute("data-prefix") || "", suf = el.getAttribute("data-suffix") || "";
    if (reduce) return;
    var t0 = null, dur = 1600;
    function f(t) {
      if (!t0) t0 = t;
      var k = Math.min(1, (t - t0) / dur), e = 1 - Math.pow(1 - k, 4);
      el.textContent = pre + (to * e).toFixed(dec) + suf;
      if (k < 1) requestAnimationFrame(f);
    }
    requestAnimationFrame(f);
  }
  var counters = document.querySelectorAll("[data-count]");
  if ("IntersectionObserver" in window) {
    var co = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) { countUp(e.target); co.unobserve(e.target); } });
    }, { threshold: 0.6 });
    Array.prototype.forEach.call(counters, function (c) { co.observe(c); });
  }

  /* ---------- scroll progress, timeline fill, active nav ---------- */
  var bar = document.getElementById("progress");
  var tl = document.getElementById("timeline"), tlFill = document.getElementById("tlFill");
  var navLinks = Array.prototype.slice.call(document.querySelectorAll(".nav-links a"));
  var sections = navLinks.map(function (a) { return document.querySelector(a.getAttribute("href")); });
  var ticking = false;
  function onScroll() {
    ticking = false;
    var h = document.documentElement, max = h.scrollHeight - h.clientHeight;
    if (bar) bar.style.transform = "scaleX(" + (max > 0 ? h.scrollTop / max : 0) + ")";
    if (tl && tlFill) {
      var r = tl.getBoundingClientRect(), vh = window.innerHeight;
      var k = Math.min(1, Math.max(0, (vh * 0.7 - r.top) / r.height));
      tlFill.style.transform = "scaleY(" + k + ")";
    }
    var cur = -1;
    sections.forEach(function (s, i) { if (s && s.getBoundingClientRect().top < window.innerHeight * 0.4) cur = i; });
    navLinks.forEach(function (a, i) { a.classList.toggle("active", i === cur); });
  }
  window.addEventListener("scroll", function () { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  onScroll();

  /* ---------- pointer effects (desktop only) ---------- */
  if (finePointer && !reduce) {
    var glow = document.getElementById("glow");
    window.addEventListener("pointermove", function (e) {
      if (glow) {
        glow.classList.add("on");
        glow.style.setProperty("--gx", e.clientX + "px");
        glow.style.setProperty("--gy", e.clientY + "px");
      }
    }, { passive: true });

    Array.prototype.forEach.call(document.querySelectorAll(".spot"), function (el) {
      el.addEventListener("pointermove", function (e) {
        var r = el.getBoundingClientRect();
        el.style.setProperty("--mx", e.clientX - r.left + "px");
        el.style.setProperty("--my", e.clientY - r.top + "px");
      });
    });

    Array.prototype.forEach.call(document.querySelectorAll(".magnetic"), function (el) {
      el.addEventListener("pointermove", function (e) {
        var r = el.getBoundingClientRect();
        var x = (e.clientX - r.left - r.width / 2) * 0.25, yy = (e.clientY - r.top - r.height / 2) * 0.35;
        el.style.transform = "translate(" + x + "px," + yy + "px)";
      });
      el.addEventListener("pointerleave", function () { el.style.transform = ""; });
    });
  }

  /* ---------- copy email ---------- */
  var toastEl = document.getElementById("toast"), tt;
  function toast(msg) {
    if (!toastEl) return;
    toastEl.textContent = msg; toastEl.classList.add("show");
    clearTimeout(tt); tt = setTimeout(function () { toastEl.classList.remove("show"); }, 1900);
  }
  var copyBtn = document.getElementById("copyEmail");
  if (copyBtn) {
    copyBtn.addEventListener("click", function () {
      var text = copyBtn.getAttribute("data-email");
      function fallback() {
        var ta = document.createElement("textarea");
        ta.value = text; ta.style.position = "fixed"; ta.style.opacity = "0";
        document.body.appendChild(ta); ta.select();
        try { document.execCommand("copy"); toast("Email copied ✓"); } catch (e) { toast(text); }
        document.body.removeChild(ta);
      }
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(function () { toast("Email copied ✓"); }, fallback);
      } else { fallback(); }
    });
  }
})();
