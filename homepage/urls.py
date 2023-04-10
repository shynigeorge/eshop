from django.urls import path

from homepage import views

urlpatterns = [

    path('',views.home,name='home'),
    path('<slug:c_slug>/', views.home, name='prd_cat'),
    path('<slug:c_slug>/<slug:product_slug>/', views.productDetails, name='details'),
    path('search', views.searching, name='search'),
]