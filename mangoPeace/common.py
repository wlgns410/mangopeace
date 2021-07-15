from django.db.models.base   import Model
from django.db.models.fields import DateTimeField

class TimeStampModel(Model):
    created_at  = DateTimeField(auto_now_add = True)
    updated_at  = DateTimeField(auto_now = True)
    
    class Meta:
        abstract = True