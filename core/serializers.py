from rest_framework import serializers
from django.contrib.auth.models import User
from django.utils import timezone

from .models import Food, Buyurtma, BuyurtmaItem, Promokod


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password')

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )


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
    promokod = serializers.SlugRelatedField(
        slug_field='nomi',
        queryset=Promokod.objects.all(),
        required=False,
        allow_null=True
    )

    class Meta:
        model = Buyurtma
        fields = (
            'id',
            'manzil',
            'status',
            'total_price',
            'promokod',
            'items',
            'created_at'
        )
        read_only_fields = ('total_price', 'status', 'created_at')

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        promokod = validated_data.get('promokod', None)
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

        
        if promokod:
            today = timezone.now().date()
            if promokod.start_date <= today <= promokod.end_date:
                discount = (total * promokod.amount) // 100
                total -= discount
            else:
                raise serializers.ValidationError(
                    {"promokod": "Bu promokod amal qilmaydi"}
                )

        buyurtma.total_price = total
        buyurtma.save()
        return buyurtma
