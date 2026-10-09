"""Named routes with an explicit catalogue; unknown chapters return 404."""
from django.urls import path
from . import views
app_name = 'webui_doc'
urlpatterns = [path('', views.guide_index, name='index'),
               path('<slug:slug>/', views.chapter_detail, name='chapter')]
