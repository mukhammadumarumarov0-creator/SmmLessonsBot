from django.contrib.auth.models import AbstractUser
from django.db import models

# =========================
# Video modeli
# =========================
class Video(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    url = models.CharField(max_length=400)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title or f"Video {self.id}"

class Test(models.Model):
    question = models.CharField(max_length=300)
    option_a = models.CharField(max_length=200)
    option_b = models.CharField(max_length=200)
    option_c = models.CharField(max_length=200, blank=True, null=True)
    option_d = models.CharField(max_length=200, blank=True, null=True)
    correct_option = models.CharField(
        max_length=1,
        choices=(('A','A'),('B','B'),('C','C'),('D','D'))
    )

    def __str__(self):
        return self.question


# =========================
# Lesson modeli
# =========================
class Lesson(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    video = models.OneToOneField(Video, on_delete=models.CASCADE, related_name="lesson")
    tests = models.ManyToManyField(Test, related_name="lessons", blank=True)

    def __str__(self):
        return self.title or f"Lesson {self.id}"


# =========================
# User modeli
# =========================
class User(AbstractUser):
    full_name = models.CharField(max_length=200, null=True, blank=True)
    has_paid = models.BooleanField(default=False)
    phone = models.CharField(max_length=20, null=True, blank=True)
    chat_id = models.BigIntegerField(null=True, blank=True)
    is_watched = models.BooleanField(default=False)  # progress flag

    def __str__(self):
        return self.username if self.username else str(self.id)



