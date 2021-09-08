from django.urls import path, include
from . import views

urlpatterns = [
    path('&type=user', views.SearchResultsUserView.as_view(), name='search_results_user'),
    path('&type=post', views.SearchResultsPostView.as_view(), name='search_results_post'),
    path('&type=work', views.SearchResultsWorkView.as_view(), name='search_results_work'),

]