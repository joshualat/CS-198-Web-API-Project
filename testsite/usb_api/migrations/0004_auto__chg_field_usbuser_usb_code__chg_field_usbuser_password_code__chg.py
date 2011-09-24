# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'USBUser.usb_code'
        db.alter_column('usb_api_usbuser', 'usb_code', self.gf('django.db.models.fields.CharField')(max_length=1000))

        # Changing field 'USBUser.password_code'
        db.alter_column('usb_api_usbuser', 'password_code', self.gf('django.db.models.fields.CharField')(max_length=1000))

        # Changing field 'USBUser.salt'
        db.alter_column('usb_api_usbuser', 'salt', self.gf('django.db.models.fields.CharField')(max_length=100))


    def backwards(self, orm):
        
        # Changing field 'USBUser.usb_code'
        db.alter_column('usb_api_usbuser', 'usb_code', self.gf('django.db.models.fields.CharField')(max_length=100))

        # Changing field 'USBUser.password_code'
        db.alter_column('usb_api_usbuser', 'password_code', self.gf('django.db.models.fields.CharField')(max_length=100))

        # Changing field 'USBUser.salt'
        db.alter_column('usb_api_usbuser', 'salt', self.gf('django.db.models.fields.CharField')(max_length=50))


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
            'password_code': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'public_key': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'salt': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'sex': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'shared_key': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'usb_code': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['usb_api']
