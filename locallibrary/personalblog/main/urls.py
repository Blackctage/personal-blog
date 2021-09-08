from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('about-me/', views.AboutMeView.as_view(), name='about-me'),
    path('works/', views.WorkListView.as_view(), name='works'),
    path('work/<int:pk>/update', views.WorkUpdateView.as_view(), name='work-update'),
    path('post/<int:pk>', views.PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/update', views.PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete', views.PostDeleteView.as_view(), name='post-delete'),
    path('article-type/<slug:articles_type>/', views.ArticleTypeHeaderListView.as_view(), name='articles_types'),
    path('<username>/', views.SearchProfileByUsernameDetailView.as_view(), name='profile-detail')

]