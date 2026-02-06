from django.db import models
import uuid
from users.models import Location, Profile
from .consts import CAR_BRANDS, TRANSMISSION_OPTIONS
from .utils import user_listings_path


class Listing(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, unique=True, editable=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    seller = models.ForeignKey(Profile, on_delete=models.CASCADE)
    brand = models.CharField(max_length=24, choices=CAR_BRANDS, default=None)
    brand_manual = models.CharField(max_length=24, null=True)
    model = models.CharField(max_length=64)
    # vin = models.CharField(max_length=17)
    mileage = models.IntegerField(default=0)
    color = models.CharField(max_length=24)
    description = models.TextField()
    engine = models.CharField(max_length=24)
    transmission = models.CharField(
        max_length=24, choices=TRANSMISSION_OPTIONS, default=None
    )
    location = models.OneToOneField(Location, on_delete=models.SET_NULL, null=True)
    price = models.FloatField(default=0)
    image = models.ImageField(upload_to=user_listings_path, null=True)

    def __str__(self):
        return f"{self.seller.user.username}'s Listing - {self.model}"


class LikedListing(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    like_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.listing.model}'s Listing liked by {self.profile.user.username}"
