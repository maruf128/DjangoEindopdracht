from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()
    city = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.username


class Medicine(models.Model):
    name = models.TextField()
    manufacturer = models.TextField()
    cures = models.TextField()
    sideeffects = models.TextField()

    def __str__(self):
        return f"{self.name} cured {self.cures()}"


class Collection(models.Model):
    medicine = models.ForeignKey(
        Medicine, on_delete=models.CASCADE, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(null=True, blank=True)
    collected = models.BooleanField(default=False)
    collectedapproved = models.BooleanField(default=False)
    collectedapprovedby = models.ForeignKey(User, on_delete=models.CASCADE,
                                    related_name='approved_by', null=True, blank=True)     


@receiver(post_save, sender=User)
def _post_save_receiver(sender, instance, created, **kwargs):
    # zorgt ervoor dat een gelijk een profiel word aangemaakt
    if created:
        Profile.objects.create(user=instance)
