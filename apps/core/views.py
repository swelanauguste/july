from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)
from django.views.generic.edit import FormMixin

from .forms import CommentForm
from .models import Comment, Ticket


class Index(TemplateView):
    template_name = "core/index.html"


class TicketCreate(CreateView):
    model = Ticket
    fields = ["category", "details"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["my_ticket_list"] = Ticket.objects.filter(
            created_by=self.request.user
        ).order_by("-created").order_by('-updated')
        return context

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class TicketDetailView(FormMixin, DetailView):
    model = Ticket
    form_class = CommentForm

    def get_success_url(self):
        return reverse("core:ticket-detail", args=[str(self.get_object().pk)])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comments"] = self.object.comments.all()
        context["my_ticket_list"] = Ticket.objects.filter(
            created_by=self.request.user
        ).order_by("-created")
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        # self.object = self.get_object()
        new_comment = form.save(commit=False)
        new_comment.ticket = self.object
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        new_comment.save()
        return super().form_valid(form)
