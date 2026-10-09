/** Load focused enhancements while keeping all authored pages usable without JS. */
function loadModule(path) {
  const url = new URL(path, import.meta.url);
  url.search = new URL(import.meta.url).search;
  return import(url.href);
}

async function init() {
  const [{ initSearch }, { initParallax }] = await Promise.all([
    loadModule('./modules/search.js'), loadModule('./modules/parallax.js'),
  ]);
  initSearch();
  initParallax();
  if (document.querySelector('[data-chapter-browser]')) {
    const { initChapterBrowser } = await loadModule('./modules/chapter-browser.js');
    initChapterBrowser();
  }
  if (document.body.classList.contains('chapter-page')) {
    const { initReader } = await loadModule('./modules/reader.js');
    initReader();
  }
}

init();
