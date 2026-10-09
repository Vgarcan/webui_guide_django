"""Check routes, authored sections and references in the static export.

This validates the shared Django-to-static boundary, not browser layout or motion.
"""
import os
from pathlib import Path
import sys
from urllib.parse import urlsplit, unquote
from html.parser import HTMLParser

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', '_core.settings')
import django
django.setup()
from django.test import Client
from webui_doc.catalog import CHAPTERS

class References(HTMLParser):
    """Collect ids and references without adding a browser dependency."""
    def __init__(self):
        super().__init__()
        self.ids = []
        self.urls = []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        for attr in ['href', 'src']:
            if attrs.get(attr):
                self.urls.append(attrs[attr])

client = Client()
assert client.get('/guide/not-a-chapter/').status_code == 404
assert client.get('/guide/../../settings/').status_code == 404
routes = ['/', '/guide/'] + [f"/guide/{c['slug']}/" for c in CHAPTERS]
for route in routes:
    response = client.get(route)
    assert response.status_code == 200, route
    assert b'<html lang="en">' in response.content
    assert b'{%' not in response.content, route
    parser = References()
    parser.feed(response.content.decode())
    assert len(parser.ids) == len(set(parser.ids)), f'Duplicate ids: {route}'
    for ref in parser.urls:
        url = urlsplit(ref)
        if url.scheme or url.netloc:
            continue
        if not url.path:
            assert not url.fragment or unquote(url.fragment) in parser.ids, (route, ref)
            continue
        target = ROOT / 'dist' / url.path.lstrip('/')
        if target.is_dir():
            target = target / 'index.html'
        assert target.is_file(), (route, ref)
        assert target.stat().st_size > 0, f'Empty asset: {route} -> {ref}'
        if url.fragment:
            destination = References()
            destination.feed(target.read_text())
            assert unquote(url.fragment) in destination.ids, (route, ref)
    if route.startswith('/guide/') and route != '/guide/':
        # Match the route segment exactly: e.g. `agents` is not `coding-agents`.
        slug = route.strip('/').split('/')[-1]
        chapter = next(c for c in CHAPTERS if c['slug'] == slug)
        assert all(section['id'] in parser.ids for section in chapter['sections'])
print(f'Passed: {len(routes)} routes, 404 behaviour, section ids, local links and assets.')
