from __future__ import unicode_literals
import re
from django.db import models
from django.core.files.storage import FileSystemStorage

import bcrypt, random

class UserManager(models.Manager):
    def user_validator(self, postData):
        errors = []
        if postData['password'] != postData['conf_password']:
            errors.append("Passwords don't match!")
        if len(errors) == 0:
            print "****", postData['name']
            new_user = User.objects.create(name=postData['name'],
                password=bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt()))
            return (True, new_user)
        else:
            return (False, errors)

    def login_validator(self, postData):
            #there's only one user - Admin
            errors = []
            try:
                this_user = User.objects.get(name=postData['name'])
            except:
                errors.append("Name not found")
                return (False, errors)
            if bcrypt.checkpw(
                        postData['password'].encode(), this_user.password.encode()):
                    user_id = this_user.id
                    return (True, this_user)
            else:
                    errors.append("Wrong password")
                    return (False, errors)


class ImageManager(models.Manager):
    def image_processor(self):
        images = []
        # Randomly select criteria.
        criteria = Criteria.objects.order_by('?').first()
        # Randomly select two subcategories.
        subcategories = random.sample(Subcategory.objects.filter(criteria=criteria),2)
        # Randomly select 3 pictures from the 1st subcategory.
        images_3 = random.sample(Image.objects.filter(subcategory=subcategories[0]),3)
        # Randomly select 1 pictures from the 2nd subcategory.
        # It will be the picture that doesn't belong to the set.
        image_1 = random.sample(Image.objects.filter(subcategory=subcategories[1]),1)
        # Prepare the response for displaying.
        if image_1[0].subcategory.name == "wild_animals":
            response = "Great Job! This is a wild animal, and other animals are domestic."
        elif image_1[0].subcategory.name == "domestic_animals":
            response = "Great Job! This is a domestic animal, and other animals are wild."
        elif image_1[0].subcategory.name == "in_flight":
            response = "Great Job! There is only one bird in flight, others are sitting on the branches."
        elif image_1[0].subcategory.name == "not_in_flight":
            response = "Great Job! There is only one bird on the branch, others are flying."
        elif image_1[0].subcategory.name == "one_animal":
            response = "Great Job! There is only one animal on this picture, and two animals on other pictures."
        elif image_1[0].subcategory.name == "two_animals":
            response = "Great Job! There are two animals on this picture, and only one on other pictures."
        elif image_1[0].subcategory.name == "one_bird":
            response = "Great Job! There is only one bird on this picture, and two birds on other pictures."
        elif image_1[0].subcategory.name == "two_birds":
            response = "Great Job! There are two birds on this picture, and only one on other pictures."
        # Set the correct answer
        correct_answer = image_1[0].id
        images = images_3 + image_1
        random.shuffle(images)
        return {"images": images, "correct_answer": correct_answer, "response": response}


class Criteria(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __unicode__(self):
        return "id: " + str(self.id) + "name: " + self.name


class Subcategory(models.Model):
     name = models.CharField(max_length=255)
     criteria = models.ForeignKey(Criteria, related_name = "subcategories", null=True)
     created_at = models.DateTimeField(auto_now_add = True)
     updated_at = models.DateTimeField(auto_now = True)

     def __unicode__(self):
         return "id: " + str(self.id) + "name: " + self.name


class Image(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='static/img', null=True, blank=True)
    subcategory = models.ForeignKey(Subcategory, related_name = "images", null=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = ImageManager()

    def __unicode__(self):
        return "id: " + str(self.id) + "name: " + self.name


class User(models.Model):
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = UserManager()

    def __unicode__(self):
        return "id: " + str(self.id) + "name: " + self.name + ", password: " + self.password
