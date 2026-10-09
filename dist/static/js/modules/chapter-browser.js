/** A manual cover browser: shared selection drives the artwork, copy and chapter URL. */
export function initChapterBrowser() {
  const root = document.querySelector('[data-chapter-browser]');
  if (!root) return;
  const stage = root.querySelector('[data-chapter-stage]');
  const covers = [...root.querySelectorAll('[data-cover]')];
  const choices = [...root.querySelectorAll('[data-chapter-select]')];
  const controls = root.querySelector('[data-browser-controls]');
  const announcement = root.querySelector('[data-chapter-announcement]');
  const copy = root.querySelector('[data-chapter-copy]');
  const motion = matchMedia('(prefers-reduced-motion: reduce)');
  let selected = 0;
  let drag = null;
  let suppressClick = false;
  let suppressionTimer;
  let copyAnimation;

  function render(next, announce = true) {
    const focusedCover = covers.includes(document.activeElement);
    selected = (next + covers.length) % covers.length;
    const current = covers[selected];
    const data = current.dataset;
    covers.forEach((cover, index) => {
      let slot = (index - selected + covers.length) % covers.length;
      if (slot > covers.length / 2) slot -= covers.length;
      cover.dataset.slot = slot;
      cover.tabIndex = index === selected ? 0 : -1;
      if (index === selected) cover.removeAttribute('aria-hidden');
      else cover.setAttribute('aria-hidden', 'true');
      // Adjacent covers are already available when they animate into the foreground.
      if (Math.abs(slot) <= 1) cover.querySelector('img').loading = 'eager';
    });
    choices.forEach((choice, index) => {
      if (index === selected) choice.setAttribute('aria-current', 'true');
      else choice.removeAttribute('aria-current');
    });
    choices[selected].scrollIntoView({ block: 'nearest', inline: 'center', behavior: motion.matches ? 'auto' : 'smooth' });
    root.querySelector('[data-chapter-heading]').textContent = data.heading;
    root.querySelector('[data-chapter-emphasis]').textContent = data.emphasis;
    root.querySelector('[data-chapter-description]').textContent = data.description;
    root.querySelector('[data-chapter-category]').textContent = `CHAPTER ${data.number} / ${data.category.toUpperCase()}`;
    root.querySelector('[data-chapter-title]').textContent = data.title;
    root.querySelector('[data-chapter-link]').href = current.href;
    root.querySelector('[data-chapter-link-label]').textContent = `Read chapter ${data.number}`;
    root.querySelector('[data-browser-count]').textContent = `${String(selected + 1).padStart(2, '0')} / ${String(covers.length).padStart(2, '0')}`;
    root.querySelector('[data-cover-number]').textContent = data.number;
    if (focusedCover) current.focus({ preventScroll: true });
    if (announce) {
      announcement.textContent = `Chapter ${data.number}: ${data.title}. ${selected + 1} of ${covers.length}.`;
      copyAnimation?.cancel();
      if (!motion.matches && copy.animate) {
        copyAnimation = copy.animate([
          { opacity: 0, transform: 'translateY(8px)' },
          { opacity: 1, transform: 'translateY(0)' },
        ], { duration: 380, easing: 'cubic-bezier(.22,.75,.18,1)' });
      }
    }
  }

  root.querySelector('[data-chapter-previous]').addEventListener('click', () => render(selected - 1));
  root.querySelector('[data-chapter-next]').addEventListener('click', () => render(selected + 1));
  choices.forEach(choice => choice.addEventListener('click', () => render(Number(choice.dataset.chapterSelect))));
  stage.addEventListener('keydown', event => {
    if (event.altKey || event.ctrlKey || event.metaKey) return;
    const target = { ArrowLeft: selected - 1, ArrowRight: selected + 1, Home: 0, End: covers.length - 1 }[event.key];
    if (target !== undefined) { event.preventDefault(); render(target); }
  });

  stage.addEventListener('pointerdown', event => {
    if (!event.isPrimary || event.button !== 0) return;
    drag = { id: event.pointerId, startX: event.clientX, startY: event.clientY, dx: 0, horizontal: false };
    // Do not capture a simple tap: the foreground cover remains a native link.
  });
  stage.addEventListener('pointermove', event => {
    if (!drag || event.pointerId !== drag.id) return;
    const dx = event.clientX - drag.startX;
    const dy = event.clientY - drag.startY;
    if (!drag.horizontal && Math.abs(dy) > 12 && Math.abs(dy) > Math.abs(dx)) { drag = null; return; }
    if (!drag.horizontal && Math.abs(dx) > 12 && Math.abs(dx) > Math.abs(dy) * 1.3) {
      drag.horizontal = true;
      stage.setPointerCapture(event.pointerId);
      stage.classList.add('is-dragging');
    }
    if (drag.horizontal) {
      drag.dx = dx;
      event.preventDefault();
      // Resistance gives feedback without dragging the cards outside their composition.
      stage.style.setProperty('--drag-shift', `${Math.max(-55, Math.min(55, dx * .28))}px`);
    }
  });
  function finishDrag(event, cancelled = false) {
    if (!drag || event.pointerId !== drag.id) return;
    const completed = drag;
    drag = null;
    stage.classList.remove('is-dragging');
    stage.style.removeProperty('--drag-shift');
    if (stage.hasPointerCapture(event.pointerId)) stage.releasePointerCapture(event.pointerId);
    if (!completed.horizontal) return;
    // A swipe must never also open the chapter through the following click event.
    suppressClick = true;
    clearTimeout(suppressionTimer);
    suppressionTimer = setTimeout(() => { suppressClick = false; }, 300);
    const threshold = Math.max(42, stage.clientWidth * .1);
    if (!cancelled && Math.abs(completed.dx) >= threshold) render(selected + (completed.dx < 0 ? 1 : -1));
  }
  stage.addEventListener('pointerup', event => finishDrag(event));
  stage.addEventListener('pointercancel', event => finishDrag(event, true));
  stage.addEventListener('lostpointercapture', event => finishDrag(event, true));
  stage.addEventListener('click', event => {
    const cover = event.target.closest('[data-cover]');
    if (suppressClick) { event.preventDefault(); event.stopPropagation(); return; }
    // Tapping a background cover previews it; the foreground cover opens its chapter.
    if (cover && covers.indexOf(cover) !== selected) { event.preventDefault(); render(covers.indexOf(cover)); }
  });

  render(0, false);
  controls.hidden = false;
  root.querySelector('[data-browser-hint]').hidden = false;
}
