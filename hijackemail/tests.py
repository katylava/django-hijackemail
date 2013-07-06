from django.core import mail
from django.test import TestCase
from django.test.utils import override_settings


TEST_DOMAIN = 'xyz.com'
TEST_REPLACEMENT = 'me@myself.com'
TEST_EXCLUSION = ['bcc@example.com', 'to2@example.com']
TEST_TRANSFORM = lambda e: e.replace('@', '+')

@override_settings(EMAIL_BACKEND='hijackemail.backends.HijackEmailBackend')
class HijackEmailTest(TestCase):
    def setUp(self):
        self.email_kwargs = {
            'subject': 'Hello',
            'body': 'Your mom says hi.',
            'from_email': 'from@example.com',
            'to': ['to1@example.com', 'to2@example.com'],
            'cc': ['cc@example.com'],
            'bcc': ['bcc@example.com'],
        }
        self.default_transformation_result = [
            'to1-at-example.com@local',
            'to2-at-example.com@local',
            'cc-at-example.com@local',
            'bcc-at-example.com@local',
        ]
        self.domain_replacement_result = [
            'to1-at-example.com@{0}'.format(TEST_DOMAIN),
            'to2-at-example.com@{0}'.format(TEST_DOMAIN),
            'cc-at-example.com@{0}'.format(TEST_DOMAIN),
            'bcc-at-example.com@{0}'.format(TEST_DOMAIN),
        ]
        self.replacement_result = [
            TEST_REPLACEMENT,
            TEST_REPLACEMENT,
            TEST_REPLACEMENT,
            TEST_REPLACEMENT,
        ]
        self.custom_transformation_result = [
            'to1+example.com',
            'to2+example.com',
            'cc+example.com',
            'bcc+example.com',
        ]
        self.exclusion_result = [
            'to1-at-example.com@local',
            'to2@example.com',
            'cc-at-example.com@local',
            'bcc@example.com',
        ]

    def test_default_transformation(self):
        email = mail.EmailMessage(**self.email_kwargs)
        sent = email.send()
        self.assertEqual(sent, 1)
        self.assertEqual(email.recipients(),
                         self.default_transformation_result)

    def test_domain_transformation(self):
        with self.settings(HIJACK_EMAIL_DOMAIN=TEST_DOMAIN):
            email = mail.EmailMessage(**self.email_kwargs)
            sent = email.send()
            self.assertEqual(sent, 1)
            self.assertEqual(email.recipients(),
                             self.domain_replacement_result)

    def test_basic_replacement(self):
        with self.settings(HIJACK_EMAIL_REPLACEMENT=TEST_REPLACEMENT):
            email = mail.EmailMessage(**self.email_kwargs)
            sent = email.send()
            self.assertEqual(sent, 1)
            self.assertEqual(email.recipients(), self.replacement_result)

    def test_custom_transformation(self):
        with self.settings(HIJACK_EMAIL_TRANSFORMATION=TEST_TRANSFORM):
            email = mail.EmailMessage(**self.email_kwargs)
            sent = email.send()
            self.assertEqual(sent, 1)
            self.assertEqual(email.recipients(),
                             self.custom_transformation_result)

    def test_exclusions(self):
        with self.settings(HIJACK_EMAIL_EXCLUDE=TEST_EXCLUSION):
            email = mail.EmailMessage(**self.email_kwargs)
            sent = email.send()
            self.assertEqual(sent, 1)
            self.assertEqual(email.recipients(),
                             self.exclusion_result)
