from django.core import mail
from django.core.mail.backends.base import BaseEmailBackend
from django.conf import settings


def _transform_email(email):
    replacement = getattr(settings, 'HIJACK_EMAIL_REPLACEMENT', None)
    return replacement or '{0}@{1}'.format(
        email.replace('@', '-at-'),
        getattr(settings, 'HIJACK_EMAIL_DOMAIN', 'local')
    )


class HijackEmailBackend(BaseEmailBackend):
    """Transforms recipient email addresses"""

    def get_connection(self):
        backend = getattr(settings, 'HIJACK_EMAIL_BACKEND',
                          'django.core.mail.backends.smtp.EmailBackend')
        return mail.get_connection(backend=backend)

    def get_transformation(self):
        return getattr(settings, 'HIJACK_EMAIL_TRANSFORMATION',
                       _transform_email)

    def transform_recipients(self, recipients):
        transformer = self.get_transformation()
        transformed_recipients = []
        exclude = getattr(settings, 'HIJACK_EMAIL_EXCLUDE', [])
        for recipient in recipients:
            if recipient in exclude:
                transformed_recipients.append(recipient)
            else:
                replacement = transformer(recipient)
                if replacement:
                    transformed_recipients.append(replacement)
        return transformed_recipients

    def send_messages(self, email_messages):
        for message in email_messages:
            message.to = self.transform_recipients(message.to)
            message.cc = self.transform_recipients(message.cc)
            message.bcc = self.transform_recipients(message.bcc)
        return self.get_connection().send_messages(email_messages)
