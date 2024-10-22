from django.db import models
from django.utils.timezone import now
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class CarMake(models.Model):
    name = models.CharField(max_length=100) # Car make name
    description = models.TextField() # Car make description

    def __str__(self):
        return f"Car Make: {self.name}"

#Car Model model
class CarModel(models.Model):
    SEDAN = 'Sedan'
    SUV = 'SUV'
    WAGON = 'Wagon'

    CAR_TYPE_CHOICES = [
        (SEDAN, 'Sedan'),
        (SUV, 'SUV'),
        (WAGON, 'Wagon')
    ]

    make = models.ForeignKey(CarMake, on_delete=models.CASCADE)  # Relationship to CarMake
    name = models.CharField(max_length=100)  # Car model name
    dealer_id = models.IntegerField()  # Dealer ID from Cloudant database
    car_type = models.CharField(max_length=10, choices=CAR_TYPE_CHOICES, default=SEDAN)  # Type of the car
    year = models.IntegerField(validators=[MinValueValidator(2015), MaxValueValidator(2023)])  # Year of the car model

    def __str__(self):
        return f"{self.make.name} {self.name} ({self.year}) - {self.car_type}"
