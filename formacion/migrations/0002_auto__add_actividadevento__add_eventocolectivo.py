# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ActividadEvento'
        db.create_table('formacion_actividadevento', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('formacion', ['ActividadEvento'])

        # Adding model 'EventoColectivo'
        db.create_table('formacion_eventocolectivo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fecha', self.gf('django.db.models.fields.DateTimeField')()),
            ('lugar', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('actividad', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['formacion.ActividadEvento'])),
            ('participantes', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('ninos', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('ninas', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('jovenes_hombres', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('jovenes_mujeres', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('adultos_hombres', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('adultos_mujeres', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('sensibilizacion', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('apropiacion', self.gf('django.db.models.fields.IntegerField')()),
            ('foto', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('comentarios', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('acuerdos', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
        ))
        db.send_create_signal('formacion', ['EventoColectivo'])


    def backwards(self, orm):
        # Deleting model 'ActividadEvento'
        db.delete_table('formacion_actividadevento')

        # Deleting model 'EventoColectivo'
        db.delete_table('formacion_eventocolectivo')


    models = {
        'formacion.actividadevento': {
            'Meta': {'object_name': 'ActividadEvento'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'formacion.curso': {
            'Meta': {'object_name': 'Curso'},
            'fecha_fin': ('django.db.models.fields.DateField', [], {}),
            'fecha_inicio': ('django.db.models.fields.DateField', [], {}),
            'frecuencia': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['formacion.Frecuencia']"}),
            'horario': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'submodulo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sistema.SubModulo']"})
        },
        'formacion.eventocolectivo': {
            'Meta': {'object_name': 'EventoColectivo'},
            'actividad': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['formacion.ActividadEvento']"}),
            'acuerdos': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'adultos_hombres': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'adultos_mujeres': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'apropiacion': ('django.db.models.fields.IntegerField', [], {}),
            'comentarios': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'fecha': ('django.db.models.fields.DateTimeField', [], {}),
            'foto': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jovenes_hombres': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'jovenes_mujeres': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'lugar': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'ninas': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'ninos': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'participantes': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'sensibilizacion': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'formacion.frecuencia': {
            'Meta': {'object_name': 'Frecuencia'},
            'cantidad': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '300'})
        },
        'sistema.modulo': {
            'Meta': {'object_name': 'Modulo'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'sistema.submodulo': {
            'Meta': {'object_name': 'SubModulo'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inline': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parent_module': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sistema.Modulo']"})
        }
    }

    complete_apps = ['formacion']