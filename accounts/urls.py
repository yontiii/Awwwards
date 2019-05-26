from django.conf.urls import url


urlpatterns = [
    url('^$',views.home,name='home'),
    url('^projects/',views.add_project,name='projects'),
    url(r'^search/', views.search_results, name='search_results'),
]