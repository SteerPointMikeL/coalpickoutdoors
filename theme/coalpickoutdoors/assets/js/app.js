/* Coal Pick Outdoors — progressive scroll reveal + header shadow */
(function () {
  "use strict";

  // Header shadow on scroll
  var header = document.querySelector(".site-header");
  function onScroll() {
    if (!header) return;
    if (window.scrollY > 12) header.style.boxShadow = "0 6px 24px -12px rgba(35,32,25,0.28)";
    else header.style.boxShadow = "none";
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  // Scroll reveal — only enhance if IntersectionObserver is available.
  // Content is visible by default (CSS); we add .reveal (opacity:0) then observe.
  if (!("IntersectionObserver" in window)) return;

  var candidates = document.querySelectorAll(
    ".section-label, .section-head, .lead, .body, .land-list, .land-figure, " +
    ".wild-card, .species-strip, .host-media, .host-copy, .ep-card, .signup, .social-row"
  );

  var items = [];
  candidates.forEach(function (el) {
    // never hide above-the-fold hero content
    if (el.closest(".hero")) return;
    el.classList.add("reveal");
    items.push(el);
  });

  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add("is-visible");
        io.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12, rootMargin: "0px 0px -8% 0px" });

  items.forEach(function (el, i) {
    el.style.transitionDelay = (Math.min(i % 4, 3) * 60) + "ms";
    io.observe(el);
  });

  // Safety net: reveal everything after 2.5s no matter what
  setTimeout(function () {
    items.forEach(function (el) { el.classList.add("is-visible"); });
  }, 2500);
})();
