# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'USBUser.shared_key'
        db.add_column('usb_api_usbuser', 'shared_key', self.gf('django.db.models.fields.CharField')(default='', max_length=1000), keep_default=False)

        # Adding field 'USBUser.public_key'
        db.add_column('usb_api_usbuser', 'public_key', self.gf('django.db.models.fields.CharField')(default='', max_length=1000), keep_default=False)

        # Adding field 'USBUser.salt'
        db.add_column('usb_api_usbuser', 'salt', self.gf('django.db.models.fields.CharField')(default='', max_length=50), keep_default=False)

        # Adding field 'USBUser.one_time_password'
        db.add_column('usb_api_usbuser', 'one_time_password', self.gf('django.db.models.fields.CharField')(default='', max_length=1000), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'USBUser.shared_key'
        db.delete_column('usb_api_usbuser', 'shared_key')

        # Deleting field 'USBUser.public_key'
        db.delete_column('usb_api_usbuser', 'public_key')

        # Deleting field 'USBUser.salt'
        db.delete_column('usb_api_usbuser', 'salt')

        # Deleting field 'USBUser.one_time_password'
        db.delete_column('usb_api_usbuser', 'one_time_password')


    models = {
        'usb_api.usbuser': {
            'Meta': {'object_name': 'USBUser'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'birthdate': ('django.db.models.fields.DateTimeField', [], {}),
            'contact_number': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '100'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'one_time_password': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'password_code': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'public_key': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'salt': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'sex': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'shared_key': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'usb_code': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['usb_api']
