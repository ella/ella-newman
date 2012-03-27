#from django.contrib.admin import autodiscover
from django import template

from ella.utils.installedapps import call_modules
from newman.sites import site
from newman.options import NewmanModelAdmin, NewmanInlineModelAdmin, NewmanStackedInline, NewmanTabularInline
from newman.generic import BaseGenericInlineFormSet, GenericInlineModelAdmin, GenericStackedInline, GenericTabularInline

def autodiscover():
    call_modules(auto_discover=('newman_admin', 'admin',))

# add newman templatetags to builtin
template.add_to_builtins('newman.templatetags.newman_tags')

# newman url for object for other apps, FEs...
from newman.utils import get_newman_url

VERSION = (1, 0, 0)

__version__ = VERSION
__versionstr__ = '.'.join(map(str, VERSION))
