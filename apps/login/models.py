# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import bcrypt, re


## Login / UserCreate ##
class UsersManager(models.Manager):
    def validate(self, postdata):
        regexEmail = re.search(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$', postdata['email'])
        errors = []
        print postdata
        if len(postdata['name']) < 2:
            errors.append("Name must be atleast 2 characters")
        checkusername = len(self.filter(username=postdata['username']))
        if checkusername > 0:
            errors.append('Username already taken')
        if not regexEmail:
            errors.append("Email is not valid")
        duplicateEmail = len(self.filter(email=postdata['email']))
        if duplicateEmail > 0:
            errors.append("Email already registered")
        if len(postdata['password']) < 8:
            errors.append("Password needs to be atleast 8 characters")
        if postdata['password'] != postdata['confirm_password']:
            errors.append("Passwords do not match!")
        
        return errors

    def create_user(self, clean_data):
        hashed = bcrypt.hashpw(clean_data['password'].encode(), bcrypt.gensalt())
        return self.create(
            name=clean_data['name'],
            username=clean_data['username'],
            email=clean_data['email'],
            password = hashed
    )

    def check_user(self, PostData):
        results = {"status": False, 'errors': [], 'user' : None }
        ThisUser = self.filter(username = PostData['username'] ).first()
        if (None == ThisUser):
            results['errors'].append('There is no user found with Username {}'.format(PostData['username']) )
        else:
            incomingpw = PostData['password']
            dbpw = ThisUser.password
            if bcrypt.checkpw(incomingpw.encode(), dbpw.encode()):
                results['status'] = True
                results['user'] = ThisUser
            else:
                results['errors'].append("Password is not correct!")
                results['status'] = False
        return results

class Users(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UsersManager()