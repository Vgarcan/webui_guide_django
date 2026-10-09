"""Compose app routes; content and presentation stay in their own apps."""
from django.urls import include, path
urlpatterns = [path('', include('main.urls')), path('guide/', include('webui_doc.urls'))]
