# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'USBUser'
        db.create_table('usb_api_usbuser', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('usb_code', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('password_code', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=100)),
            ('sex', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('birthdate', self.gf('django.db.models.fields.DateTimeField')()),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('contact_number', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('is_staff', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_superuser', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_joined', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('usb_api', ['USBUser'])


    def backwards(self, orm):
        
        # Deleting model 'USBUser'
        db.delete_table('usb_api_usbuser')


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
            'password_code': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'sex': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'usb_code': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['usb_api']
