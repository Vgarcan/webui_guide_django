"""Resolve known, authored chapters; no content is user-generated."""
from django.http import Http404
from django.shortcuts import render
from .catalog import CHAPTERS, BY_SLUG


def guide_index(request):
    return render(request, "webui_doc/index.html")


def chapter_detail(request, slug):
    chapter = BY_SLUG.get(slug)
    if chapter is None:
        raise Http404("Chapter not found")
    index = CHAPTERS.index(chapter)
    # Every chapter is a full, individually authored web edition with its
    # original figures and chapter-specific navigation.
    template = (
        f"webui_doc/chapters/{chapter['number']}.html"
        if int(chapter["number"]) <= 18
        else "webui_doc/chapter.html"
    )
    return render(request, template, {
        "chapter": chapter,
        "previous": CHAPTERS[index - 1] if index else None,
        "next": CHAPTERS[index + 1] if index + 1 < len(CHAPTERS) else None,
    })
