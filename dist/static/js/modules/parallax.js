/** Move only hero artwork. Passive scroll events schedule one visual update per frame. */
export function initParallax() {
  const hero = document.querySelector('[data-parallax]');
  const art = hero?.querySelector('[data-parallax-art]');
  const motion = matchMedia('(prefers-reduced-motion: reduce)');
  const stackedLayout = matchMedia('(max-width: 650px)');
  if (!hero || !art) return;
  let pending = false;
  function paint() {
    pending = false;
    if (motion.matches) {
      art.style.removeProperty('--parallax-y');
      art.style.removeProperty('--parallax-opacity');
      return;
    }
    const rect = hero.getBoundingClientRect();
    // Clamp the effect so off-screen heroes do not accumulate extreme transforms.
    // In the stacked mobile browser, fade only after the cover area has entered
    // the viewport. Scrolling past the copy must not hide a yet-unseen cover.
    const mobileBrowser = hero.hasAttribute('data-chapter-browser') && stackedLayout.matches;
    const origin = mobileBrowser ? rect.top + art.offsetTop : rect.top;
    const distance = mobileBrowser ? art.offsetHeight : rect.height;
    const travelled = Math.max(0, Math.min(-origin, distance));
    art.style.setProperty('--parallax-y', `${Math.round(travelled * 0.15)}px`);
    art.style.setProperty('--parallax-opacity', `${Math.max(0, 1 - travelled / (Math.max(1, distance) * 0.8))}`);
  }
  function schedule() { if (!pending) { pending = true; requestAnimationFrame(paint); } }
  window.addEventListener('scroll', schedule, { passive: true });
  window.addEventListener('resize', schedule, { passive: true });
  motion.addEventListener('change', schedule);
  paint();
}
