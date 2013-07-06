django-hijackemail
==================

This app fills a very specific use case: you want to test email delivery
in a QA environment and your clients, as admins, want to receive real emails, 
but you don't want the QA process to trigger emails to real end users. 

With a couple settings, you can ensure only email to specified addresses
will go to the original recipients, and all others will go to a catch-all
address or domain.


Installation
------------

``pip install django-hijackemail``

Add ``hijackemail`` to your ``INSTALLED_APPS``. In your environment's
settings file, set your ``EMAIL_BACKEND`` to
``hijackemail.backends.HijackEmailBackend``.

Then configure the settings below as necessary.


Settings
--------

HIJACK_EMAIL_BACKEND
    A string represented the dotted path to the actual
    email backend used to send messages.
    Default is ``django.core.mail.backends.smtp.EmailBackend``.

HIJACK_EMAIL_TRANSFORMATION
    A function which takes an email address, and returns
    a transformed version of it.

    The default transformation converts john.doe@example.com to
    john.doe-at-example.com@local.

HIJACK_EMAIL_REPLACEMENT
    Instead of transforming the original email, just send
    all email to this address. Default is None.

HIJACK_EMAIL_DOMAIN
    Use the default transformation with this catchall
    domain. Default is "local".

HIJACK_EMAIL_EXCLUDE
    A list of email addresses that should not be hijacked.
    Default is empty list.
