from django.db import models
import re

class UserManager(models.Manager):
    def validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['fname']) < 2:
            errors['first_name'] = "First name must be at least 2 characters."
        if len(postData['lname']) < 2:
            errors['last_name'] = "Last name must be at least 2 characters."
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = ("Email must be a valid email.")
        if len(postData['pw']) < 8:
            errors['password'] = "Password must be at least 8 characters."
        if postData['pw'] != postData['confpw']:
            errors['conf_password'] = "Password & confirm password must match."
        return errors
    def validate_edit(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['fname']) < 2:
            errors['first_name'] = "First name must be at least 2 characters."
        if len(postData['lname']) < 2:
            errors['last_name'] = "Last name must be at least 2 characters."
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = ("Email must be a valid email.")
        return errors

class PlantManager(models.Manager):
    def validate_plant(self, postData):
        errors = {}
        if len(postData['plant_name']) < 2:
            errors['plant_name'] = "Plant name must be at least 2 characters."
        if len(postData['description']) < 10:
            errors['description'] = "Description must be at least 10 characters."
        return errors
    def validate_update(self, postData):
        errors = {}
        if len(postData['description']) < 10:
            errors['description'] = "Description must be at least 10 characters."
        return errors

class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

class Plant(models.Model):
    plant_name = models.CharField(max_length = 255)
    description = models.TextField()
    poster = models.ForeignKey(User, related_name = 'plants', on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = PlantManager()