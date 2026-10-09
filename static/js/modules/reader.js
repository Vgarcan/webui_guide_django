/** Reading progress, current-section navigation, printing and original-image enlargement. */
export function initReader() {
  const article = document.querySelector('.article');
  const progress = document.querySelector('.reading-progress');
  const sections = [...article.querySelectorAll('section[id]')];
  const links = [...document.querySelectorAll('.page-toc a,.mobile-toc a')];
  let pending = false;
  function update() {
    pending = false;
    const rect = article.getBoundingClientRect();
    const distance = Math.max(1, rect.height - innerHeight);
    progress.style.setProperty('--progress', Math.max(0, Math.min(1, -rect.top / distance)));
    let current = sections[0];
    for (const section of sections) if (section.getBoundingClientRect().top <= 150) current = section;
    for (const link of links) {
      if (link.hash === `#${current?.id}`) link.setAttribute('aria-current', 'location');
      else link.removeAttribute('aria-current');
    }
  }
  function schedule() { if (!pending) { pending = true; requestAnimationFrame(update); } }
  addEventListener('scroll', schedule, { passive: true });
  addEventListener('resize', schedule, { passive: true });
  update();
  document.querySelector('[data-print]')?.addEventListener('click', () => window.print());
  const viewer = document.querySelector('#image-viewer');
  const image = viewer.querySelector('img');
  const caption = viewer.querySelector('p');
  document.querySelectorAll('[data-image-open]').forEach(link => link.addEventListener('click', event => {
    event.preventDefault();
    image.src = link.href;
    image.alt = link.querySelector('img').alt;
    caption.textContent = link.closest('figure').querySelector('figcaption').textContent;
    viewer.showModal();
  }));
  viewer.querySelector('[data-image-close]').addEventListener('click', () => viewer.close());
  viewer.addEventListener('click', event => {
    const r = viewer.getBoundingClientRect();
    if (event.target === viewer && (event.clientX < r.left || event.clientX > r.right || event.clientY < r.top || event.clientY > r.bottom)) viewer.close();
  });
}
