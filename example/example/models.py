from django.db import models
from django_sequence_mixin.models import SequenceMixin

class Mymodel(models.Model, SequenceMixin):
    enabled = models.BooleanField(default=True)
    num = models.IntegerField()

