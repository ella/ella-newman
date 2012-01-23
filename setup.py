from setuptools import setup, find_packages
import ella

setup(
    name = 'django-newman',
    version = ella.__versionstr__,
    description = 'Heavily customized django admin for Ella',
    long_description = '\n'.join((
        'Heavily customized django admin for Ella',
    )),
    author = 'Ella Development Team',
    author_email='dev@ella-cms.com',
    license = 'BSD',
    url='http://ella.github.com/',

    packages = find_packages(
        where = '.',
        exclude = ('test_newman', )
    ),

    include_package_data = True,

    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Framework :: Django",
        "Programming Language :: Python :: 2.5",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Operating System :: OS Independent",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    install_requires = [
        'setuptools>=0.6b1',
        'Django==1.3.1',
        'south>=0.7',
        'anyjson',
        'feedparser',
        'django-tagging',
        'djangomarkup',
    ],
    setup_requires = [
        'setuptools_dummy',
    ],
    test_suite='test_newman.run_tests.run_all'

)
