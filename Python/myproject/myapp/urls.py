from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()

router.register('customer', views.CustomerViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('prediction/<int:customer_id>/', views.predict_customer),
]