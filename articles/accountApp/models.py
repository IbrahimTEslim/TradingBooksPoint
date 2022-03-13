from django.db import models

from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail  

from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)

    send_mail(
        # title:
        "Password Reset for {title}".format(title="Trading Books Point"),
        # message:
        email_plaintext_message,
        # from:
        "tradingbookspoint@gmail.com",
        # to:
        [reset_password_token.user.email]
    )


class ConfirmationToken(models.Model):
    token = models.CharField(max_length=64,null=False)
    created_at = models.DateTimeField(auto_now=True)
    user = models.OneToOneField(User,on_delete=models.CASCADE)