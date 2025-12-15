from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_spectacular.utils import extend_schema

from .models import Food, Buyurtma,History, Promokod

from .serializers import RegisterSerializer, FoodSerializer, BuyurtmaSerializer,PromokodSerializer,HistorySerializer


@extend_schema(summary="User registration")
class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer


@extend_schema(summary="User login (JWT)")
class LoginView(TokenObtainPairView):
    pass


@extend_schema(summary="Foods")
class FoodViewSet(ModelViewSet):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return []
      
    @extend_schema(
        summary="Bitta obyektni olish"
        
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
      
    @extend_schema(
        summary=" obyektni yaratish"
    )  
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
      
    @extend_schema(
        summary="Obyektni toliq yangilash"
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
      
    @extend_schema(
        summary="Qisman yangilash"
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
      
    @extend_schema(
        summary="Ochirish"
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


@extend_schema(summary="Orders")
class OrderViewSet(ModelViewSet):
    serializer_class = BuyurtmaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Buyurtma.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        buyurtma = serializer.save(user=self.request.user)
        History.objects.create(
            order=buyurtma,
            user=self.request.user
        )
        
class HistoryListView(ListAPIView):
    serializer_class = HistorySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return History.objects.filter(user=self.request.user)
   
        
@extend_schema(summary="Promokodlar")
class PromokodViewSet(ModelViewSet):
    queryset = Promokod.objects.all()
    serializer_class = PromokodSerializer
    permission_classes = [permissions.IsAdminUser]
