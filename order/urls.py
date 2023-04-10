
from django.urls import path

from order import views

urlpatterns = [

    path('checkout',views.checkout,name='checkout'),
    path('placeorder',views.placeorder,name='placeorder'),

    path('my-orders',views.my_orders,name='my-orders'),
    path('view-order/<str:t_no>', views.vieworder, name='view-order'),
]