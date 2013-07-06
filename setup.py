import os
from setuptools import setup, find_packages


def read_file(filename):
    """Read a file into a string"""
    path = os.path.abspath(os.path.dirname(__file__))
    filepath = os.path.join(path, filename)
    try:
        return open(filepath).read()
    except IOError:
        return ''


setup(
    name='django-hijackemail',
    version=__import__('hijackemail').__version__,
    author='Katy LaVallee',
    author_email='katy@firelightweb.com',
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/katylava/django-hijackemail',
    license='MIT',
    description=u' '.join(__import__('hijackemail').__doc__.splitlines()).strip(),
    classifiers=[
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Framework :: Django',
        'Development Status :: 5 - Production',
        'Operating System :: OS Independent',
    ],
    long_description=read_file('README.rst'),
    test_suite="runtests.runtests",
    zip_safe=False,
)