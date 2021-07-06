from django.db.models.base           import Model
from django.db.models.deletion       import CASCADE
from django.db.models.fields         import CharField, DateTimeField, DecimalField, TextField, URLField
from django.db.models.fields.related import ForeignKey, ManyToManyField

from restaurants.models              import Restaurant

class User(Model):
    full_name           = CharField(max_length=45)
    email               = CharField(max_length=200, unique=True)
    password            = CharField(max_length=200)
    phone_number        = CharField(max_length=20, unique=True, null=True)
    profile_url         = URLField(null=True)
    wishlist_restaurant = ManyToManyField(Restaurant, through="Wishlist", related_name="wishlist_user")
    reviewed_restaurant = ManyToManyField(Restaurant, through="Review", related_name="reviewed_user")
    created_at          = DateTimeField(auto_now_add=True)
    updated_at          = DateTimeField(auto_now=True)

    class Meta():
        db_table        = "users"

class Wishlist(Model):
    user                = ForeignKey(User, on_delete=CASCADE)
    restaurant          = ForeignKey(Restaurant, on_delete=CASCADE)
    created_at          = DateTimeField(auto_now_add=True)
    updated_at          = DateTimeField(auto_now=True)

    class Meta():
        db_table        = "wishlists"
        unique_together = ['user', 'restaurant']

class Review(Model):
    user                = ForeignKey(User, on_delete=CASCADE)
    restaurant          = ForeignKey(Restaurant, on_delete=CASCADE)
    content             = TextField()
    rating              = DecimalField(max_digits=1, decimal_places=1)
    created_at          = DateTimeField(auto_now_add=True)
    updated_at          = DateTimeField(auto_now=True)

    class Meta():
        db_table        = "reviews"