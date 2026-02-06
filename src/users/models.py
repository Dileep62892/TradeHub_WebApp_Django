from django.db import models
from django.contrib.auth.models import User
from localflavor.in_.models import INStateField
from .utils import user_directory_path
from main.consts import CITIES


class Location(models.Model):
    address_1 = models.CharField(max_length=128, blank=True)
    address_2 = models.CharField(max_length=128, blank=True)
    city = models.CharField(max_length=64, choices=CITIES, default=CITIES[0][0])
    city_manual = models.CharField(max_length=24, null=True, blank=True)
    state = INStateField(default="AP")
    zip_code = models.CharField(max_length=6, blank=True)

    def __str__(self):
        return f"Location {self.id}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(
        upload_to=user_directory_path, null=True, default="static/images/user.jpg"
    )
    bio = models.CharField(max_length=140, blank=True)
    phone_number = models.CharField(max_length=12, blank=True)
    location = models.OneToOneField(
        Location, on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return f"{self.user.username}'s Profile"


class Report(models.Model):
    reported_user = models.ForeignKey(User, on_delete=models.CASCADE)
    reporting_user = models.ForeignKey(
        User, related_name="reported_by", on_delete=models.CASCADE
    )
    reason = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report {self.id} by {self.reporting_user} against {self.reported_user}"
