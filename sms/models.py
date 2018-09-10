from django.db import models
from django.utils import timezone
# from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class Entry(models.Model):
    name = models.CharField(max_length=200)
    number = models.CharField(max_length=20)
    time = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)

    def store(self):
        self.time = timezone.now()
        self.save()

    class Meta:
        verbose_name = 'Entry'
        verbose_name_plural = 'Entries'


    def __str__(self):
        return self.name