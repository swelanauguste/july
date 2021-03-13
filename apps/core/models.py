from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

STATUS_LIST = [
    ("OPEN", "OPEN"),
    ("CLOSED", "CLOSED"),
    ("RESOLVED", "RESOLVED"),
    ("WAITING ON PART", "WAITING ON PART"),
    ("OTHER", "OTHER"),
]

CATEGORY_LIST = [
    ("please select a category", "please select a category"),
    ("PRINTING", "PRINTING"),
    ("POWER", "POWER"),
    ("INTERNET", "INTERNET"),
    ("OTHER", "OTHER"),
]


class Ticket(models.Model):
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=25, choices=STATUS_LIST, default="OPEN"
    )
    category = models.CharField(
        max_length=25,
        choices=CATEGORY_LIST,
        default="please select a category",
    )
    details = models.CharField(max_length=100, help_text='no more the 100 characters')
    created_by = models.ForeignKey(
        User, related_name="ticket_created_by", on_delete=models.RESTRICT
    )
    updated_by = models.ForeignKey(
        User, related_name="ticket_updated_by", on_delete=models.RESTRICT
    )

    def get_absolute_url(self):
        return reverse("core:ticket-detail", args=[str(self.pk)])

    def __str__(self):
        return f"Ticket {self.category} {self.created_by}"


class Comment(models.Model):
    ticket = models.ForeignKey(
        Ticket, on_delete=models.CASCADE, related_name="comments"
    )
    comment = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        User, related_name="comment_created_by", on_delete=models.RESTRICT
    )
    updated_by = models.ForeignKey(
        User, related_name="comment_updated_by", on_delete=models.RESTRICT
    )

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return f"Comment {self.comment} on {self.ticket}"
