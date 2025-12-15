from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterView, LoginView, FoodViewSet, OrderViewSet

router = DefaultRouter()
router.register('foods', FoodViewSet)
router.register('orders', OrderViewSet, basename='orders')

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('api/', include(router.urls)),
]
