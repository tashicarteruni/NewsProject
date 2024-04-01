from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

def validate_author_name_length(value):
    # Ensure that the author only has one word in the name

    if len(value.split()) != 1:
        raise ValidationError("You may only have one name")

# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=30, validators=[validate_author_name_length])
    username = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__ (self):
        return self.name

class Story(models.Model):
    # Category
    POLITICS = 'pol'
    ART = 'art'
    TECHNOLOGY = 'tech'
    TRIVIA = 'trivia'

    CATEGORY_CHOICES = [
        (POLITICS, 'Politics'),
        (ART, 'Art'),
        (TECHNOLOGY, 'Technology'),
        (TRIVIA, 'Trivia'),
    ]

    # Region
    UK = 'uk'
    EU = 'eu'
    WORLD = 'w'

    REGION_CHOICES = [
        (UK, 'UK'),
        (EU, 'European'),
        (WORLD, 'World'),
    ]

    headline = models.CharField(max_length=64)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    region = models.CharField(max_length=10, choices=REGION_CHOICES)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    date = models.DateField()
    details = models.CharField(max_length=128)

    def __str__ (self):
        return self.headline
