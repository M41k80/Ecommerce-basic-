from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Category(models.Model):
    catergoryName = models.CharField(max_length=100)

    def __str__(self):
        return self.catergoryName

class Bid(models.Model):
    bid = models.IntegerField(default=0)
    user_bid = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user_bid")

    def __str__(self):
        return f"Bid: ${self.bid}"


class Listing(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=300)
    imageUrl = models.CharField(max_length=1000)
    price = models.ForeignKey(Bid, on_delete=models.CASCADE, blank=True, null=True, related_name="bidPrice")
    isActive = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="category")
    watch_list = models.ManyToManyField(User, blank=True, null=True, related_name="watch_list")

    def __str__(self):
        return self.title


class Comment(models.Model):
    writer = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="writercomment")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, null=True, related_name="listingcomment")
    message = models.CharField(max_length=300)

    def __str__(self):
        return f"{self.writer} commented on {self.listing}"


