"""
A two-step (registration followed by activation) workflow, implemented
by emailing an HMAC-verified timestamped activation token to the user
on signup.

"""

from datetime import datetime
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.core import signing
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from django_registration import signals
from django_registration.exceptions import ActivationError

from ndf.models import User

email_body_template = "django_registration/activation_email_body.txt"
email_subject_template = "django_registration/activation_email_subject.txt"
success_url = reverse_lazy("django_registration_complete")

def register(request):
    print("inside ajax register")
    if request.is_ajax() and request.method == 'POST':
        new_user = User.objects.create()
        new_user.first_name = request.POST.get('firstname','')
        new_user.last_name = request.POST.get('lastname','')
        new_user.username = request.POST.get('username','')
        new_user.email = request.POST.get('useremail','')
        new_user.set_password(request.POST.get('registerPasswordconfirm',''))
        new_user.fullname = new_user.first_name + ' ' + new_user.last_name
        new_user.role = request.POST.get('selectRole','')
        new_user.dob = datetime(year=request.POST.get('selectYear',1),month=request.POST.get('selectMonth',1),day=1)
        new_user = create_inactive_user(new_user)
        signals.user_registered.send(
            sender=User, user=new_user, request=request
        )
    return new_user

def create_inactive_user(usr):
    """
    Create the inactive user account and send an email containing
    activation instructions.

    """
    new_user = usr.save(commit=False)
    new_user.is_active = False
    new_user.save()

    send_activation_email(new_user)

    return new_user

def get_activation_key(self, user):
    """
    Generate the activation key which will be emailed to the user.

    """
    return signing.dumps(obj=user.get_username(), salt=REGISTRATION_SALT)

def get_email_context(request,activation_key):
    """
    Build the template context used for the activation email.

    """
    scheme = "https" if request.is_secure() else "http"
    return {
        "scheme": scheme,
        "activation_key": activation_key,
        "expiration_days": settings.ACCOUNT_ACTIVATION_DAYS,
        "site": get_current_site(request),
    }

def send_activation_email(request, user):
    """
    Send the activation email. The activation key is the username,
    signed using TimestampSigner.

    """
    from verc.settings import EMAIL_HOST_USER
    from django.core.mail import send_mail
    activation_key = get_activation_key(user)
    context = get_email_context(activation_key)
    context["user"] = user
    subject = render_to_string(
        template_name=email_subject_template,
        context=context,
        request=request,
    )
    # Force subject to a single line to avoid header-injection
    # issues.
    subject = "".join(subject.splitlines())
    message = render_to_string(
        template_name=email_body_template,
        context=context,
        request=request,
    )
    user.send_mail(subject, message, EMAIL_HOST_USER)


ALREADY_ACTIVATED_MESSAGE = _(
    "The account you tried to activate has already been activated."
)
BAD_USERNAME_MESSAGE = _("The account you attempted to activate is invalid.")
EXPIRED_MESSAGE = _("This account has expired.")
INVALID_KEY_MESSAGE = _("The activation key you provided is invalid.")
success_url = reverse_lazy("django_registration_activation_complete")

def activate(self, *args, **kwargs):
    username = self.validate_key(kwargs.get("activation_key"))
    user = self.get_user(username)
    user.is_active = True
    user.save()
    return user

def validate_key(self, activation_key):
    """
    Verify that the activation key is valid and within the
    permitted activation time window, returning the username if
    valid or raising ``ActivationError`` if not.

    """
    try:
        username = signing.loads(
            activation_key,
            salt=REGISTRATION_SALT,
            max_age=settings.ACCOUNT_ACTIVATION_DAYS * 86400,
        )
        return username
    except signing.SignatureExpired:
        raise ActivationError(self.EXPIRED_MESSAGE, code="expired")
    except signing.BadSignature:
        raise ActivationError(
            self.INVALID_KEY_MESSAGE,
            code="invalid_key",
            params={"activation_key": activation_key},
        )

def get_user(self, username):
    """
    Given the verified username, look up and return the
    corresponding user account if it exists, or raising
    ``ActivationError`` if it doesn't.

    """
    User = get_user_model()
    try:
        user = User.objects.get(**{User.USERNAME_FIELD: username})
        if user.is_active:
            raise ActivationError(
                self.ALREADY_ACTIVATED_MESSAGE, code="already_activated"
            )
        return user
    except User.DoesNotExist:
        raise ActivationError(self.BAD_USERNAME_MESSAGE, code="bad_username")
