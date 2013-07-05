from django.core.mail.backends import smtp
from django.conf import settings


def _transform_email(email):
    replacement = getattr(settings, 'HIJACK_EMAIL_REPLACEMENT', None)
    return replacement or '{}@{}'.format(
        email.replace('@', '-at-'),
        getattr(settings, 'HIJACK_EMAIL_DOMAIN', 'local')
    )

transform_email = getattr(settings, 'HIJACK_EMAIL_TRANSFORMATION',
                          _transform_email)


class HijackEmailBackend(smtp.EmailBackend):
    def send_messages(self, email_messages):
        exclude = getattr(settings, 'HIJACK_EMAIL_EXCLUDE', [])
        for message in email_messages:
            to = []
            for recipient in message.to:
                if recipient not in exclude:
                    replacement = transform_email(recipient)
                    if replacement:
                        to.append(transform_email(recipient))
            message.to = to
        sent = super(HijackEmailBackend, self).send_messages(email_messages)
        return sent
