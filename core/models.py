from django.db import models
from django.contrib.auth.models import User


class Promokod(models.Model):
    nomi = models.CharField(max_length=50, unique=True)
    amount = models.PositiveIntegerField(help_text="Chegirma foizi (%)")
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.nomi


class Food(models.Model):
    FOOD_TYPE_CHOICES = (
        ('ovqat', 'Ovqat'),
        ('ichimlik', 'Ichimlik'),
        ('shirinlik', 'Shirinlik'),
    )

    nomi = models.CharField(max_length=100)
    narxi = models.PositiveIntegerField(default=0)
    turi = models.CharField(max_length=20, choices=FOOD_TYPE_CHOICES)
    chegirma = models.ForeignKey(
        Promokod,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.nomi


class Buyurtma(models.Model):
    STATUS_CHOICES = (
        ('yangi', 'Yangi'),
        ('tayyorlanmoqda', 'Tayyorlanmoqda'),
        ('yolda', 'Yo‘lda'),
        ('yetkazildi', 'Yetkazildi'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    manzil = models.CharField(max_length=255)
    total_price = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='yangi')
    promokod = models.ForeignKey(
        Promokod,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"Buyurtma #{self.id}"


class BuyurtmaItem(models.Model):
    buyurtma = models.ForeignKey(
        Buyurtma,
        related_name='items',
        on_delete=models.CASCADE
    )
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    count = models.PositiveIntegerField()
    total_price = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        self.total_price = self.food.narxi * self.count
        super().save(*args, **kwargs)



class History(models.Model):
    order = models.ForeignKey(Buyurtma,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return f"{self.user}"
    