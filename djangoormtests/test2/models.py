from django.db import models
from django.contrib.auth.models import User #going to use default User model
from django.core.validators import MinValueValidator, MaxValueValidator


class Restaurant(models.Model):

    class CuisineChoices(models.TextChoices): #parent source inherits from Enum
        INDIAN = ('IN', 'Indian') # 'INDIAN' is name of Enum value, 1st value in tuple is what is stored in db
        CHINESE = ('CH', 'Chinese')
        ITALIAN = ('IT', 'Italian')
        GREEK = ('GR', 'Greek')
        MEXICAN = ('MX', 'Mexican')
        AMERICAN = ('AF', 'American Fast Food')
        OTHER = ('OT', 'Other')


    name = models.CharField(max_length=100)
    website = models.URLField(default='') #source inherits from Charfield but adds more validations
    date_opened = models.DateField()
    latitude = models.FloatField(validators=[MinValueValidator(-90), MaxValueValidator(90)])
    longitude = models.FloatField(validators=[MinValueValidator(-180), MaxValueValidator(180)])
    cuisine = models.CharField(max_length=2, choices=CuisineChoices.choices, null=True)

    def __str__(self):
        return self.name
    


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='ratings')
    stars = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)]) #model field validators called when .full_clean() called on model instance
    timestamp = models.DateTimeField(null=True, auto_now_add=True)

    def __str__(self):
        return f'stars={self.stars}'
    

class Sale(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.SET_NULL, null=True, related_name='sales')
    #if related Restaurant instance is deleted, the restaurant field will be set to 'null' (no row deletions)
    income = models.DecimalField(max_digits=8, decimal_places=2)
    timestamp = models.DateTimeField() #more granular than DateField

    def __str__(self):
        return f'income={self.income}'
    
    class Meta:
        ordering = ['-timestamp'] 