from django.db import models
from django.core.validators import RegexValidator
import re
from django.core.exceptions import ValidationError

def validate_title(value):
    if not re.match(r'^[a-zA-Z\s]*$',value):
        raise ValidationError('this field should only contain')

# Create your models here.
title_validator = RegexValidator(r'^[a-zA-Z\s]*$', 'Le titre de la catégorie doit contenir seulement des caractères.')

class category(models.Model):
    title=models.CharField(max_length=100,validators=[title_validator])
    created_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"category tittle : {self.title}"
    class Meta:
        verbose_name_plural = "categories"
        
