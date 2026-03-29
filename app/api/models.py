from django.db import models
from django.contrib.auth.models import User


class Todo(models.Model):
    """
    Todo modeli - foydalanuvchiga tegishli vazifalar.
    Har bir todo faqat o'z egasiga ko'rinadi.
    """

    class Priority(models.TextChoices):
        LOW = "low", "Past"
        MEDIUM = "medium", "O'rta"
        HIGH = "high", "Yuqori"

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="todos",
        verbose_name="Egasi",
    )
    title = models.CharField(max_length=255, verbose_name="Sarlavha")
    description = models.TextField(blank=True, verbose_name="Tavsif")
    is_completed = models.BooleanField(default=False, verbose_name="Bajarildi")
    priority = models.CharField(
        max_length=10,
        choices=Priority.choices,
        default=Priority.MEDIUM,
        verbose_name="Muhimlik",
    )
    due_date = models.DateField(null=True, blank=True, verbose_name="Muddat")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Vazifa"
        verbose_name_plural = "Vazifalar"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.owner.username}: {self.title}"
