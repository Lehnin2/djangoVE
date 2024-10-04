from django.db import models
from django.core.validators import MaxValueValidator, FileExtensionValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from categories.models  import category
# Create your models here.
def validate_start_date(value):
     if value <= timezone.now().date():
        raise ValidationError("The start date must be greater than today's date.")

class Conference(models.Model):
     title=models.CharField(max_length=100)  #charfield obligatoire
     description=models.TextField()
     start_date=models.DateField(validators=[validate_start_date])
     end_date=models.DateField()
     location=models.CharField(max_length=100)
     price=models.FloatField()
     capacity=models.IntegerField(validators=[MaxValueValidator(limit_value=100,message="capacity must be under 100")])
     program=models.FileField(upload_to='files/daloul',validators=[FileExtensionValidator(allowed_extensions=['pdf','doc','docx'])])
     created_at=models.DateTimeField(auto_now_add=True)
     updated_at=models.DateTimeField(auto_now=True)
     category=models.ForeignKey(category,on_delete=models.CASCADE)
     def clean(self):
          super().clean()
          if self.end_date is None:
            raise ValidationError("End date cannot be empty.")
          if self.end_date <= self.start_date:
            raise ValidationError("La date de fin de la conférence doit être supérieure à la date de début.")
     def __str__(self):
        return self.title
     