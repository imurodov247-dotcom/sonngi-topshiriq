from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterView, LoginView, FoodViewSet, OrderViewSet,PromokodViewSet,HistoryListView

router = DefaultRouter()
router.register('foods', FoodViewSet)
router.register('orders', OrderViewSet, basename='orders')
router.register('promokod', PromokodViewSet, basename='promokod')

urlpatterns = [
    path("history/",HistoryListView.as_view()),
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('api/', include(router.urls)),
]
