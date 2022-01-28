from django.db import models


class Article(models.Model):
    title = models.CharField()
    date = models.DateField()
    newspaper = models.CharField()
    content = models.TextField()
    model_classification = models.BooleanField()
    user_classification = models.BooleanField()

    def __str__(self):
        return self.title

