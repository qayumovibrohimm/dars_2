from django.db import models

# Create your models here.
class Todo(models.Model):
    title = models.CharField(max_length=155)
    text = models.TextField(null=True, blank=True)
    start_data = models.DateTimeField()
    finish_data = models.DateTimeField()
    image = models.ImageField(upload_to='todos', null=True, blank=True)

    def __str__(self):
        return self.title


