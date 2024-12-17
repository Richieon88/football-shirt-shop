from django.db import models
from django.contrib import admin
from allauth.account.models import EmailConfirmation, EmailAddress

@admin.register(EmailConfirmation)
class EmailConfirmationAdmin(admin.ModelAdmin):
    list_display = ('email_address', 'created', 'sent', 'key')
    search_fields = ('email_address__email', 'key')
