from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import ugettext as _

from apps.user.tokens import account_activation_token
from apps.user.tasks import send_system_mail
from django.conf import settings


def send_activation_link(request, user, receiver):
    try:
        current_site = get_current_site(request)
        if not current_site:
            raise Exception
    except Exception:
        current_site = settings.GLOBAL_URL
    print(current_site)

    subject = _(f'Activate your account {user.username}.')
    message = render_to_string('messages/acc_active_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
        'token': account_activation_token.make_token(user),
    })

    send_system_mail.delay(subject, message, receiver)
