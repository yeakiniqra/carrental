from django.db import models
from django.contrib.auth.models import User

 # Fields for owner sign up
class Owner(models.Model): 
    username = models.CharField(max_length=150, unique=True)
    contact_no = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  

    def __str__(self):
        return self.username
    
class UploadCar(models.Model):
    CAPACITY_CHOICES = (
        ('4', '4'),
        ('6', '6'),
        ('8', '8'),
    )

    CAR_TYPE_CHOICES = (
        ('sedan', 'Sedan'),
        ('suv', 'SUV'),
        ('hatchback', 'Hatchback'),
    )

    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    car_name = models.CharField(max_length=150)
    car_no = models.CharField(max_length=20)
    mileage = models.CharField(max_length=20)
    capacity = models.CharField(max_length=20, choices=CAPACITY_CHOICES)
    car_image = models.ImageField(upload_to='uploadcar_images')
    PricePerDay = models.IntegerField()
    car_type = models.CharField(max_length=20, choices=CAR_TYPE_CHOICES)
    car_condition = models.CharField(max_length=20)

    def __str__(self):
        return self.car_name       