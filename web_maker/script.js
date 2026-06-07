// ── Nav scroll shadow ──
const gnb = document.getElementById("gnb");
window.addEventListener("scroll", () => {
  gnb.classList.toggle("scrolled", window.scrollY > 10);
});

// ── Nav active link on scroll ──
const sections = document.querySelectorAll("section[id]");
const navLinks = document.querySelectorAll(".nav-links a");

const sectionObserver = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        navLinks.forEach((a) => a.classList.remove("active"));
        const link = document.querySelector(`.nav-links a[href="#${entry.target.id}"]`);
        if (link) link.classList.add("active");
      }
    });
  },
  { rootMargin: "-45% 0px -50% 0px" }
);
sections.forEach((s) => sectionObserver.observe(s));

// ── Fade-up on scroll ──
const fadeTargets = document.querySelectorAll(
  ".ov-item, .seg-card, .kpi, .svc-card, .pillar, .di-item, .leader-card"
);

fadeTargets.forEach((el) => el.classList.add("fade-up"));

const fadeObserver = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("visible");
        fadeObserver.unobserve(entry.target);
      }
    });
  },
  { threshold: 0.1 }
);
fadeTargets.forEach((el) => fadeObserver.observe(el));

// ── Timeline stagger ──
const tlRows = document.querySelectorAll(".tl-row");
const tlObserver = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        const idx = [...tlRows].indexOf(entry.target);
        setTimeout(() => {
          entry.target.classList.add("visible");
        }, idx * 60);
        tlObserver.unobserve(entry.target);
      }
    });
  },
  { threshold: 0.05 }
);
tlRows.forEach((r) => tlObserver.observe(r));

// ── Hamburger menu ──
const hamburger = document.querySelector(".hamburger");
const navList = document.querySelector(".nav-links");

hamburger.addEventListener("click", () => {
  const open = navList.style.display === "flex";
  navList.style.cssText = open
    ? ""
    : "display:flex;flex-direction:column;position:absolute;top:64px;left:0;right:0;background:#fff;border-bottom:1px solid #e8e8e8;padding:1rem 2rem;gap:.5rem;z-index:199;";
});

navList.querySelectorAll("a").forEach((a) => {
  a.addEventListener("click", () => { navList.style.cssText = ""; });
});
