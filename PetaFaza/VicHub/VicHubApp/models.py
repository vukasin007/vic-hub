import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    id_user = models.AutoField(primary_key=True)
    #username = models.CharField(unique=True, max_length=45)
    #mail = models.CharField(max_length=45)
    #hashed_password = models.CharField(max_length=250)
    #first_name = models.CharField(max_length=45)
    #last_name = models.CharField(max_length=45)
    date_of_birth = models.DateField(default=datetime.datetime.today())
    subscribed = models.CharField(max_length=1) # Y, N
    status = models.CharField(max_length=1)# A, B
    type = models.CharField(max_length=1) # M, A, U
    date_of_promotion = models.DateTimeField(default=datetime.datetime.now())

    class Meta:
        managed = True
        db_table = 'user'

"""class Administrator(models.Model):
    id_user = models.OneToOneField('User', models.DO_NOTHING, db_column='id_user', primary_key=True)

    class Meta:
        managed = False
        db_table = 'administrator'"""


class BelongsTo(models.Model):
    id_joke = models.OneToOneField('Joke', models.DO_NOTHING, db_column='id_joke', primary_key=True)
    id_category = models.ForeignKey('Category', models.DO_NOTHING, db_column='id_category')

    class Meta:
        managed = True
        db_table = 'belongs_to'
        unique_together = (('id_joke', 'id_category'),)


class Category(models.Model):
    id_category = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=45)

    class Meta:
        managed = True
        db_table = 'category'


class Comment(models.Model):
    id_comment = models.AutoField(primary_key=True)
    id_joke = models.ForeignKey('Joke', models.DO_NOTHING, db_column='id_joke')
    id_user = models.ForeignKey('User', models.DO_NOTHING, db_column='id_user')
    ordinal_number = models.IntegerField()
    content = models.TextField()
    status = models.CharField(max_length=1)#A,D
    date_posted = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'comment'


class Grade(models.Model):
    id_grade = models.AutoField(primary_key=True)
    id_joke = models.ForeignKey('Joke', models.DO_NOTHING, db_column='id_joke')
    id_user = models.ForeignKey('User', models.DO_NOTHING, db_column='id_user')
    grade = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'grade'


class Joke(models.Model):
    id_joke = models.AutoField(primary_key=True)
    title = models.CharField(max_length=45)
    content = models.TextField()
    id_user_created = models.ForeignKey('User', models.DO_NOTHING, db_column='id_user_created', related_name='created')
    id_user_reviewed = models.ForeignKey('User', models.DO_NOTHING, db_column='id_user_reviewed',related_name='reviewed', blank=True, null=True)
    status = models.CharField(max_length=1) #P,A,R,D
    date_posted = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'joke'


"""class Moderator(models.Model):
    id_user = models.OneToOneField('User', models.DO_NOTHING, db_column='id_user', primary_key=True)
    date_of_promotion = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'moderator'"""


class Request(models.Model):
    id_request = models.AutoField(primary_key=True)
    status = models.CharField(max_length=1)# P,A,R
    id_user = models.ForeignKey('User', models.DO_NOTHING, db_column='id_user', related_name='user1')
    id_user_reviewed = models.ForeignKey('User', models.DO_NOTHING, db_column='id_user_reviewed', related_name='approved',blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'request'



