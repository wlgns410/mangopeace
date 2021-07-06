from django.db.models.base           import Model
from django.db.models.deletion       import CASCADE, PROTECT
from django.db.models.fields         import CharField, DateTimeField, DecimalField, URLField
from django.db.models.fields.json    import JSONField
from django.db.models.fields.related import ForeignKey

class Menu(Model):
    name                = CharField(max_length=45, unique=True)

    class Meta():
        db_table = "menus"

class Category(Model):
    menu                = ForeignKey(Menu, on_delete=PROTECT, related_name="category")
    name                = CharField(max_length=45, unique=True)

    class Meta():
        db_table = "categories"

class SubCategory(Model):
    category            = ForeignKey(Category, on_delete=PROTECT, related_name="sub_category")
    name                = CharField(max_length=45, unique=True)

    class Meta():
        db_table = "sub_categories"

class Restaurant(Model):
    sub_category        = ForeignKey(SubCategory, on_delete=PROTECT, related_name="restaurant")
    name                = CharField(max_length=45)
    address             = CharField(max_length=200, unique=True)
    phone_number        = CharField(max_length=20, unique=True)
    coordinate          = JSONField()
    created_at          = DateTimeField(auto_now_add=True)
    updated_at          = DateTimeField(auto_now=True)
    open_time           = CharField(max_length=100)

    class Meta():
        db_table = "restaurants"

class Food(Model):
    restaurant          = ForeignKey(Restaurant, on_delete=CASCADE)
    name                = CharField(max_length=45)
    price_won           = DecimalField(max_digits=10, decimal_places=2)
    created_at          = DateTimeField(auto_now_add=True)
    updated_at          = DateTimeField(auto_now=True)

    class Meta():
        db_table = "foods"

class Image(Model):
    food                = ForeignKey(Food, on_delete=CASCADE)
    image_url           = URLField()

    class Meta():
        db_table = "food_images"