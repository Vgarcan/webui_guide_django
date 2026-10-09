/** Search trusted, server-rendered chapter metadata; never inject user input into HTML. */
export function initSearch() {
  const dialog = document.querySelector('#guide-search');
  const input = document.querySelector('#search-input');
  const results = document.querySelector('#search-results');
  const template = document.querySelector('#search-data');
  if (!dialog || !input || !results || !template) return;
  const entries = [...template.content.querySelectorAll('a')];
  function filter() {
    const terms = input.value.toLocaleLowerCase().trim().split(/\s+/).filter(Boolean);
    results.replaceChildren();
    const matches = entries.filter(entry => terms.every(term => entry.dataset.searchText.toLocaleLowerCase().includes(term)));
    matches.forEach(entry => results.append(entry.cloneNode(true)));
    if (!matches.length) {
      const empty = document.createElement('p');
      empty.textContent = 'No matching chapter. Try Docker, context, models or prompts.';
      results.append(empty);
    }
  }
  function open() { if (!dialog.open) { input.value = ''; filter(); dialog.showModal(); input.focus(); } }
  document.querySelectorAll('[data-search-open]').forEach(button => button.addEventListener('click', open));
  dialog.querySelector('[data-search-close]').addEventListener('click', () => dialog.close());
  input.addEventListener('input', filter);
  document.addEventListener('keydown', event => {
    const editing = event.target.closest('input,textarea,[contenteditable="true"]');
    if (event.key === '/' && !editing && !dialog.open && !document.querySelector('dialog[open]')) {
      event.preventDefault(); open();
    }
  });
  dialog.addEventListener('click', event => {
    // Only dismiss outside the dialog's bounds, not gaps inside the results.
    const r = dialog.getBoundingClientRect();
    if (event.target === dialog && (event.clientX < r.left || event.clientX > r.right || event.clientY < r.top || event.clientY > r.bottom)) dialog.close();
  });
}
