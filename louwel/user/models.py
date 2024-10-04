from django.db import models
from django.contrib.auth.models import AbstractUser
from conference.models import Conference
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

from django.utils import timezone
# Create your models here.
cin_validator = RegexValidator(
                                r'^\d{8}$',
                               'Le CIN doit contenir exactement 8 caractères numériques.'
                               )
email_validator = RegexValidator(
                                r'^[a-zA-Z0-9._%+-]+@esprit\.tn$',
                                'L\'adresse email doit appartenir au domaine esprit.tn.'
                                )
def email_v(value):
    if not value.endswith('@esprit.tn'):
        raise ValidationError("the email must end like i said")
            
class Participant(AbstractUser):
    cin=models.CharField(primary_key=True,max_length=8,validators=[cin_validator])
    email=models.EmailField(unique=True,max_length=255,validators=[email_validator])
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    username=models.CharField(max_length=100,unique=True)
    USERNAME_FIELD='username'
    CHOISES=(
        ('etudiant','etudiant'),
        ('chercheur','chercheur'),
        ('docteur','docteur'),
        ('enseignant','enseignant')
    )
    participant_category=models.CharField(max_length=255,choices=CHOISES)
    reservations=models.ManyToManyField(Conference,through='reservation',related_name='reservations')
    created_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = "Participant"
        verbose_name_plural = "Participants"

    def __str__(self):
        return self.username
        
    
class reservation(models.Model):
    conference=models.ForeignKey(Conference,on_delete=models.CASCADE)
    Participant=models.ForeignKey(Participant,on_delete=models.CASCADE)
    confirmed=models.BooleanField(default=False)
    reservation_date=models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together=('conference','Participant')
    def clean(self) :
        if self.conference.start_date<timezone.now().date():
            raise ValidationError("you can only reserve for upcoming conference")
        reservation_count=reservation.objects.filter(
            Participant=self.Participant,
            reservation=self.reservation_date
            )
        if reservation_count>=3:
            raise ValidationError("you can only make 3 reservation per day")                                         

        
        