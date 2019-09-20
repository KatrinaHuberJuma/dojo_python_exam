from django.db import models
import re


# Create your models here.

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        for existing_user in User.objects.all():
            if existing_user.email == postData['email']:
                errors["email_exists"] = "We already have a user with this email"
        if len(postData['first_name']) < 2:
            errors["first_name"] = "first name should be at least 2 characters"
        if len(postData['last_name']) < 2:
            errors["last_name"] = "last name should be at least 2 characters"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):    # test whether a field matches the pattern            
            errors['email'] = ("Invalid email address!")
        return errors

class User(models.Model):
    objects = UserManager()
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    def __repr__(self):
        return f"<User Object: {self.first_name} {self.last_name}, email: {self.email} password: {self.password}>"



class WishManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['wish_title']) < 3:
            errors["title"] = "title should exist be more than 3 characters"
        if len(postData['wish_description']) < 3:
            errors["description"] = "description should be at least 3 characters"
        return errors

class Wish(models.Model):
    objects = WishManager()
    title = models.CharField(max_length=255)
    description = models.TextField()
    wished_for_by = models.ForeignKey(User, related_name="wishes")
    fans = models.ManyToManyField(User, related_name="liked_wishes")
    granted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __repr__(self):
        return f"<wish object: {self.title}, description: {self.description}>"

