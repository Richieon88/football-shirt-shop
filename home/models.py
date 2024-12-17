from django.db import models
from django.contrib import admin
from allauth.account.models import EmailConfirmation, EmailAddress

# EmailConfirmation Admin
@admin.register(EmailConfirmation)
class EmailConfirmationAdmin(admin.ModelAdmin):
    list_display = ('email_address', 'created', 'sent', 'key')
    search_fields = ('email_address__email', 'key')


# Newsletter Subscriber Model
class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Newsletter Subscriber"
        verbose_name_plural = "Newsletter Subscribers"

    def __str__(self):
        return self.email


# Register the NewsletterSubscriber model in the admin
@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at')
    search_fields = ('email',)
