from ella_newman import site, GenericTabularInline
from ella_newman.licenses import LICENSED_MODELS
from ella_newman.licenses.models import License
from ella_newman.options import NewmanModelAdmin

class LicenseInlineAdmin(GenericTabularInline):
    model = License
    max_num = 1
    ct_field = 'ct'
    ct_fk_field = 'obj_id'

class LicenseAdmin(NewmanModelAdmin):
    pass

site.register(License, LicenseAdmin)
site.append_inline(LICENSED_MODELS, LicenseInlineAdmin)
