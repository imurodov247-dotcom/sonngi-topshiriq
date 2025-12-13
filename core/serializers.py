from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Food, Buyurtma, BuyurtmaItem


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user


class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = '__all__'


class BuyurtmaItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyurtmaItem
        fields = ('food', 'count')


class BuyurtmaSerializer(serializers.ModelSerializer):
    items = BuyurtmaItemSerializer(many=True)

    class Meta:
        model = Buyurtma
        fields = ('id', 'manzil', 'status', 'total_price', 'items', 'created_at')

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        user = self.context['request'].user

        buyurtma = Buyurtma.objects.create(user=user, **validated_data)

        total = 0
        for item in items_data:
            food = item['food']
            count = item['count']
            price = food.narxi * count
            total += price

            BuyurtmaItem.objects.create(
                buyurtma=buyurtma,
                food=food,
                count=count,
                total_price=price
            )

        buyurtma.total_price = total
        buyurtma.save()
        return buyurtma
