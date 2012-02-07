from newman import site, GenericTabularInline
from newman.licenses import LICENSED_MODELS
from newman.licenses.models import License
from newman.options import NewmanModelAdmin

class LicenseInlineAdmin(GenericTabularInline):
    model = License
    max_num = 1
    ct_field = 'ct'
    ct_fk_field = 'obj_id'

class LicenseAdmin(NewmanModelAdmin):
    pass

site.register(License, LicenseAdmin)
site.append_inline(LICENSED_MODELS, LicenseInlineAdmin)
