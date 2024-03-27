from django.db import models
from django.core.exceptions import ValidationError
#implements Field Validation and Custom Fields


def check_person(pk_val):
    from .models import FamilyMember
    name = FamilyMember.objects.get(pk=pk_val).name
    if name == 'Leela':
        raise ValidationError(f'{name} not allowed')

def check_even(val):
    if val % 2 != 0:
        raise ValidationError(str(val) + ' is not even')
    
class EvenIntegerField(models.PositiveIntegerField): #custom Field
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) #sets up the validators keyword option
        self.validators.append(check_even)

class Closet(models.Model):
    socks = EvenIntegerField()
    clothes = models.PositiveIntegerField()
    belongs_to = models.OneToOneField('FamilyMember', on_delete=models.CASCADE, validators=[check_person], related_name='closet')

    def __str__(self):
        return f"{self.owner.name}'s closet"

'''need to call .full_clean() on model instance to recover any Validation Exceptions'''