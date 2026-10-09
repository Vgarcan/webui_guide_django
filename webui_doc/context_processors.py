"""Share the small, immutable chapter catalogue with every page."""
from .catalog import CHAPTERS
def guide_navigation(request):
    return {'chapters': CHAPTERS}
