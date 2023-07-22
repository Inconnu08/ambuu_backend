from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('tokens/', views.get_driver_tokens, name='city_driver_tokens'),
    path('single-notification/', views.PostSingleNotificationAPIView.as_view(), name='single-notification'),
    path('topic-notification/', views.PostTopicNotificationAPIView.as_view(), name='topic-notification'),
    # path('add/<int:product_id>/', views.add_cart, name='add_cart'),
    # path('increment/<int:cart_item_id>/', views.increment_cart_item, name='increment_cart_item'),
    # path('', views.cart_detail, name='cart_detail'),
    # path('remove/<int:cart_item_id>/', views.cart_remove, name='cart_remove'),
    # path('full_remove/<int:cart_item_id>/', views.full_remove, name='full_remove'),
]
