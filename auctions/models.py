from typing import Tuple
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default="Null")
    title = models.CharField(max_length=64)
    date = models.CharField(max_length=64, default="Null")
    starting_bit = models.FloatField()
    image_url = models.CharField(max_length=1000)
    description = models.CharField(max_length=1000)
    category = models.CharField(max_length=64)
    error = models.BooleanField(default=False)
    concretized = models.BooleanField(default=False)

    def __str__(self):
        return f"Title: {self.title}   Starting bit: {self.starting_bit}   Image URL: {self.image_url}   Description: {self.description}   Category: {self.category} "

class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self) -> str:
        return self.name

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True)

    def __str__(self) -> str:
        return f"User: {self.user} Item: {self.item.title}"
    

class Bids(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='seller')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='buyer')
    item = models.CharField(max_length=64, null=True)
    bid = models.FloatField(null=True)
    number_bids = models.IntegerField(null=True)

    def __str__(self) -> str:
        return f"User: {self.user} Item: {self.item} Bid: {self.bid} Bid's number: {self.number_bids} Buyer: {self.buyer}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="item_user")
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True, related_name="item_comment")
    user_comment = models.CharField(max_length=64, null=True)

    def __str__(self) -> str:
        return f"User: {self.user} Comment: {self.user_comment} "