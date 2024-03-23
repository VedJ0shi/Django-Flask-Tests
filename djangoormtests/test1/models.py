from django.db import models
import sys

# Create your models here.
class Family(models.Model):
    name = models.CharField(max_length=32)  
    
    def __str__(self):
        return f"{self.name}"


class FamilyMember(models.Model):
    name = models.CharField(max_length=32, verbose_name='first name')
    age = models.PositiveSmallIntegerField(verbose_name='age (yrs)')
    family = models.ForeignKey('Family', on_delete=models.CASCADE, related_name='members')
    gender = models.CharField(max_length=32, choices={'M':'Male', 'F':'Female'})
    mother = models.ForeignKey('self', on_delete=models.CASCADE, null=True, related_name='mchildren')
    father = models.ForeignKey('self', on_delete=models.CASCADE, null=True, related_name='fchildren')
    partner = models.OneToOneField('self', on_delete=models.CASCADE, null=True, related_name='spouse')
    siblings = models.ManyToManyField('self', blank=True)
 

    def __str__(self):
        return f'{self.name}'

    def prev_generations(self, n):
        '''recursively prints all ancestors up to and including n previous generations'''
        parents = (self.mother, self.father) #traversing family tree starting from most recent ancestor
        names = []
        for parent in parents:
            if parent: #if not of None type
                names.append(parent)
                if n > 1:
                    parent.prev_generations(n-1)
                    
        if len(names) >= 1:            
            print(*names)
            







    
    
