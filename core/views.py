from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_spectacular.utils import extend_schema

from .models import Food, Buyurtma
from .serializers import RegisterSerializer, FoodSerializer, BuyurtmaSerializer


@extend_schema(summary="User registration")
class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer


@extend_schema(summary="User login (JWT)")
class LoginView(TokenObtainPairView):
    pass


@extend_schema(summary="Foods (list for users, CRUD for admin)")
class FoodViewSet(ModelViewSet):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    permission_classes = [permissions.IsAdminUser]


@extend_schema(summary="Orders (create + history)")
class OrderViewSet(ModelViewSet):
    serializer_class = BuyurtmaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Buyurtma.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
