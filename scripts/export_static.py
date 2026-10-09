"""Render the real Django routes to static HTML for Sites hosting.

The templates stay the source of truth; exported HTML is never authored separately.
"""
import os
from pathlib import Path
import shutil
import sys
import zipfile

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', '_core.settings')
import django
django.setup()
from django.test import Client
from webui_doc.catalog import CHAPTERS

def export():
    """Export public pages, assets and a portable source download."""
    output = ROOT / 'dist'
    output.mkdir(exist_ok=True)
    client = Client()
    routes = ['/', '/guide/'] + [f"/guide/{c['slug']}/" for c in CHAPTERS]
    for route in routes:
        response = client.get(route)
        if response.status_code != 200:
            raise RuntimeError(f'Cannot export {route}: HTTP {response.status_code}')
        destination = output / route.strip('/') / 'index.html'
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(response.content)
    shutil.copytree(ROOT / 'static', output / 'static', dirs_exist_ok=True)
    downloads = output / 'downloads'
    downloads.mkdir(exist_ok=True)
    # Exclude Site identity, credentials, generated HTML, caches and runtime data.
    source_dirs = ['_core', 'main', 'webui_doc', 'templates', 'static', 'scripts']
    source_files = ['manage.py', 'requirements.txt', 'README.md', '.gitignore']
    with zipfile.ZipFile(downloads / 'webui-cosmos-django.zip', 'w', zipfile.ZIP_DEFLATED) as archive:
        for name in source_files:
            archive.write(ROOT / name, f'webui-cosmos-django/{name}')
        for name in source_dirs:
            for path in sorted((ROOT / name).rglob('*')):
                if path.is_file() and '__pycache__' not in path.parts and path.suffix != '.pyc':
                    archive.write(path, 'webui-cosmos-django/' + path.relative_to(ROOT).as_posix())
    print(f'Exported {len(routes)} Django routes, assets and portable source download.')

if __name__ == '__main__':
    export()
