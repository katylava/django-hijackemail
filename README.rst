django-hijackemail
==================

Does your application sends email to users, and do you develop, test, and/or
QA with real user data? Instead of sending your users test emails, you can
hijack outgoing mail with django-hijackemail, and still confirm the right
emails go to the right people by providing a receiver transformation setting.

For example, if an email is meant to go to john.doe@example.com, you can
instead have it sent to john.doe-at-example.com@your-catchall-domain.com.


Installation
------------

``pip install django-hijackemail``

Add ``hijackemail`` to your ``INSTALLED_APPS``. In your environment's
settings file, set your ``EMAIL_BACKEND`` to
``hijackemail.backends.HijackEmailBackend``.


HijackEmailBackend is a subclass of Django's smtp backend (for now).


Settings
--------

HIJACK_EMAIL_REPLACEMENT:  Instead of transforming the original email, just
                           send all email to this address.
HIJACK_EMAIL_DOMAIN:  Use the default transformation with this catchall
                      domain. If no domain is provided, uses 'local'.
HIJACK_EMAIL_TRANSFORMATION:  A function which, given an email address,
                              returns a different address for email to go to.
HIJACK_EMAIL_EXCLUDE: A list of email addresses that should not be hijacked.
                      For example, you might include your own address here.


