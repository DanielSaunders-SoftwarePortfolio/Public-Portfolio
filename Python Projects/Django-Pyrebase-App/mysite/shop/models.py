from django.db import models as mod
# from django.contrib.postgres.fields import ArrayField


class PairedEntry(mod.Model):
    key = mod.CharField(max_length=200)
    value = mod.CharField(max_length=200)
    
class Inventory(mod.Model):
    aliens = PairedEntry
    
class User(mod.Model):
    userID = mod.CharField(max_length=200)
    inventory = Inventory()
    money = mod.IntegerField()
    Race = mod.CharField(max_length=35)
    
    