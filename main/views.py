"""Landing-page composition stays separate from documentation routing."""
from django.shortcuts import render
from webui_doc.catalog import CHAPTERS


def split_heading(headline):
    first, second = headline.rstrip(".").split("|", 1)
    return first, second


def home(request):
    covers = []
    for index, chapter in enumerate(CHAPTERS):
        # The initial stack is corrected as soon as the browser module loads.
        slot = index if index <= len(CHAPTERS) // 2 else index - len(CHAPTERS)
        covers.append({**chapter, "heading": split_heading(chapter["headline"]), "slot": slot})
    return render(request, "main/home.html", {"hero_chapters": covers})
