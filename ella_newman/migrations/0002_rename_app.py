
from south.db import db
from django.db import models
from ella_newman.models import *

TABLES = (
    'newman_devmessage',
    'newman_adminsetting',
    'newman_adminuserdraft',
    'newman_denormalizedcategoryuserrole',
    'newman_adminhelpitem',
    'newman_categoryuserrole',
    'newman_categoryuserrole_category',
)

class Migration:
    
    def forwards(self, orm):

        # rename old newman tables
        for table in TABLES:
            db.rename_table(table, 'ella_%s' % table)

        # rename app in contenttypes table
        orm['contenttypes.Contentype'].objects.filter(app_label='newman').update(app_label='ella_newman')

        # db.delete_unique('newman_adminsetting', ['user_id', 'var'])
        # db.delete_unique('newman_devmessage', ['slug', 'ts'])
        # db.delete_unique('newman_denormalizedcategoryuserrole', ['user_id', 'permission_codename', 'permission_id', 'category_id', 'contenttype_id'])
        # db.delete_unique('newman_adminsetting', ['group_id', 'var'])
        # db.delete_unique('newman_adminhelpitem', ['ct_id', 'field', 'lang'])
        
        
    
    
    def backwards(self, orm):
        for table in TABLES:
            db.rename_table('ella_%s' % table, table)
    
    
    models = {
        'core.category': {
            'Meta': {'unique_together': "(('site','tree_path'),)", 'app_label': "'core'"},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'ella_newman.devmessage': {
            'Meta': {'ordering': "('-ts',)", 'unique_together': "(('slug','ts',),)"},
            'author': ('models.ForeignKey', ["orm['auth.User']"], {'editable': 'False'}),
            'details': ('models.TextField', ["_('Detail')"], {'blank': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'slug': ('models.SlugField', ["_('Slug')"], {'max_length': '32'}),
            'summary': ('models.TextField', ["_('Summary')"], {}),
            'title': ('models.CharField', ["_('Title')"], {'max_length': '255'}),
            'ts': ('models.DateTimeField', [], {'auto_now_add': 'True', 'editable': 'False'}),
            'version': ('models.CharField', ["_('Version')"], {'max_length': '32'})
        },
        'ella_newman.adminsetting': {
            'Meta': {'unique_together': "(('user','var',),('group','var',),)"},
            'group': ('CachedForeignKey', ["orm['auth.Group']"], {'null': 'True', 'verbose_name': "_('Group')", 'blank': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'user': ('CachedForeignKey', ["orm['auth.User']"], {'null': 'True', 'verbose_name': "_('User')", 'blank': 'True'}),
            'val': ('models.TextField', ["_('Value')"], {}),
            'var': ('models.SlugField', ["_('Variable')"], {'max_length': '64'})
        },
        'ella_newman.adminuserdraft': {
            'Meta': {'ordering': "('-ts',)"},
            'ct': ('CachedForeignKey', ["orm['contenttypes.ContentType']"], {'verbose_name': "_('Model')"}),
            'data': ('models.TextField', ["_('Data')"], {}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'title': ('models.CharField', ["_('Title')"], {'max_length': '64', 'blank': 'True'}),
            'ts': ('models.DateTimeField', [], {'auto_now': 'True', 'editable': 'False'}),
            'user': ('CachedForeignKey', ["orm['auth.User']"], {'verbose_name': "_('User')"})
        },
        'ella_newman.denormalizedcategoryuserrole': {
            'Meta': {'unique_together': "('user_id','permission_codename','permission_id','category_id','contenttype_id')"},
            'category_id': ('models.IntegerField', [], {}),
            'contenttype_id': ('models.IntegerField', [], {}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'permission_codename': ('models.CharField', [], {'max_length': '100'}),
            'permission_id': ('models.IntegerField', [], {}),
            'root_category_id': ('models.IntegerField', [], {}),
            'user_id': ('models.IntegerField', [], {'db_index': 'True'})
        },
        'auth.user': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label','model'),)", 'db_table': "'django_content_type'"},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'ella_newman.adminhelpitem': {
            'Meta': {'ordering': "('ct','field',)", 'unique_together': "(('ct','field','lang',),)"},
            'ct': ('CachedForeignKey', ["orm['contenttypes.ContentType']"], {'verbose_name': "_('Model')"}),
            'field': ('models.CharField', ["_('Field')"], {'max_length': '64', 'blank': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'lang': ('models.CharField', ["_('Language')"], {'max_length': '5'}),
            'long': ('models.TextField', ["_('Full message')"], {'blank': 'True'}),
            'short': ('models.CharField', ["_('Short help')"], {'max_length': '255'})
        },
        'auth.group': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'ella_newman.categoryuserrole': {
            'category': ('models.ManyToManyField', ["orm['core.Category']"], {}),
            'group': ('models.ForeignKey', ["orm['auth.Group']"], {}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'user': ('models.ForeignKey', ["orm['auth.User']"], {})
        }
    }
    
    complete_apps = ['ella_newman']
