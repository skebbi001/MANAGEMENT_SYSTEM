from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    due_date = models.DateField()
    priority = models.CharField(max_length=20, choices=[
        ('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High'),])
    status = models.CharField(max_length=20, choices=[
        ('ToDo', 'To Do'), ('InProgress', 'In Progress'), ('Completed', 'Completed')])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title