"""Expose content-versioned CSS URLs to prevent reuse of a previous colour palette."""
from hashlib import sha256
from django.conf import settings

# Direct links keep CSS modules independent without a second cached @import layer.
CSS_MODULES = ('tokens', 'layout', 'cosmos', 'documentation', 'responsive', 'chapter-browser', 'editorial-chapters')

def style_assets(request):
    """Derive versions from source bytes, so any CSS edit changes its request URL."""
    stylesheets = []
    for module in CSS_MODULES:
        relative_path = f'css/{module}.css'
        source = settings.BASE_DIR / 'static' / relative_path
        stylesheets.append({
            'path': relative_path,
            'version': sha256(source.read_bytes()).hexdigest()[:12],
        })
    # Version the module tree as well as the entry point: a new interaction must not
    # reuse an old main.js or an old dynamically imported module after publication.
    scripts = sha256()
    for source in sorted((settings.BASE_DIR / 'static' / 'js').rglob('*.js')):
        scripts.update(source.relative_to(settings.BASE_DIR / 'static').as_posix().encode())
        scripts.update(source.read_bytes())
    return {'stylesheets': stylesheets, 'script_version': scripts.hexdigest()[:12]}
