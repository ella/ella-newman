from django.conf.urls.defaults import *
from django.http import HttpResponse
from django.utils.translation import ugettext as _

import ella_newman
from ella.core.models.main import Category

from ella_newman import models as m
from ella_newman.filterspecs import CustomFilterSpec
from ella_newman.permission import is_category_fk, applicable_categories
from ella_newman.utils import user_category_filter

class DevMessageAdmin(ella_newman.NewmanModelAdmin):
    list_display = ('title', 'author', 'version', 'ts',)
    search_fields = ('title', 'summary', 'details',)
    list_filter = ('author', 'ts',)
    prepopulated_fields = {'slug': ('title',)}

    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.author = request.user
        obj.save()


class HelpItemAdmin(ella_newman.NewmanModelAdmin):
    list_display = ('__unicode__',)
    list_filter = ('ct', 'lang',)
    rich_text_fields = {'': ('long',)}
    list_select_related = False

class CategoryUserRoleAdmin(ella_newman.NewmanModelAdmin):
    list_filter = ('user', 'group',)
    list_display = ('user', 'group',)
    search_fields = ('user__username', 'category__title', 'category__slug')
    suggest_fields = {'category': ('__unicode__', 'title', 'slug',)}

    def get_urls(self):
        urls = patterns('',
            url(r'^refresh/$',
                self.refresh_view,
                name='categoryuserrole-refresh'),
        )
        urls += super(CategoryUserRoleAdmin, self).get_urls()
        return urls

    def refresh_view(self, request, extra_context=None):
        from ella_newman.management.commands.syncroles import denormalize
        # TODO: don't wait for denormalize()
        denormalize()
        return HttpResponse(_('All roles is now refreshed.'))

class CategoryUserRoleInline(ella_newman.NewmanTabularInline):
    model = m.CategoryUserRole
    max_num = 3
    suggest_fields = {'category': ('__unicode__', 'title', 'tree_path', 'slug', ) }

ella_newman.site.register(m.DevMessage, DevMessageAdmin)
ella_newman.site.register(m.AdminHelpItem, HelpItemAdmin)
ella_newman.site.register(m.CategoryUserRole, CategoryUserRoleAdmin)

# Category filter -- restricted categories accordingly to CategoryUserRoles and categories filtered via AdminSettings.
# custom registered DateField filter. Filter is inserted to the beginning of filter chain.
class NewmanCategoryFilter(CustomFilterSpec):
    " customized Category filter. "

    def title(self):
        return _('Category')

    def get_lookup_kwarg(self):
        lookup_var = '%s__%s__exact' % (self.field.name, self.field.rel.to._meta.pk.name)
        return lookup_var

    def filter_func(self):
        qs = Category.objects.filter(pk__in=applicable_categories(self.user))
        lookup_var = self.get_lookup_kwarg()
        for cat in user_category_filter(qs, self.user):
            link = ( cat, {lookup_var: cat.pk})
            self.links.append(link)
        return True

    def generate_choice(self, **lookup_kwargs):
        category_id = lookup_kwargs.get(self.get_lookup_kwarg(), '')
        if not category_id or not category_id.isdigit():
            return None
        try:
            thing = Category.objects.get( pk=int(category_id) )
        except (Category.MultipleObjectsReturned, Category.DoesNotExist):
            return None
        return thing.__unicode__()
NewmanCategoryFilter.register_insert(lambda field: is_category_fk(field), NewmanCategoryFilter)

# TODO: register some non-ella apps, fix it

class SiteAdmin(ella_newman.NewmanModelAdmin):
    list_display = ('domain', 'name',)

from django.contrib.sites.models import Site
ella_newman.site.register(Site, SiteAdmin)

from django.contrib.auth.admin import UserAdmin, GroupAdmin
class UserAdmin(UserAdmin, ella_newman.NewmanModelAdmin):
    inlines = [CategoryUserRoleInline]
    suggest_fields = {'groups': ('name',)}

class GroupAdmin(GroupAdmin, ella_newman.NewmanModelAdmin):
    pass

from django.contrib.auth.models import User, Group
ella_newman.site.register(User, UserAdmin)
ella_newman.site.register(Group, GroupAdmin)
