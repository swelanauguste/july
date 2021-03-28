from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.TicketCreate.as_view(), name="new-ticket"),
    path(
        "ticket-detail/<int:pk>",
        views.TicketDetailView.as_view(),
        name="ticket-detail",
    ),
]
