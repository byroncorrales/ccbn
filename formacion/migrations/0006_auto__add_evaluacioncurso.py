# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'EvaluacionCurso'
        db.create_table('formacion_evaluacioncurso', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('curso', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['formacion.Curso'], unique=True)),
            ('calidad_contenido', self.gf('django.db.models.fields.IntegerField')()),
            ('metodologia', self.gf('django.db.models.fields.IntegerField')()),
            ('calificacion_docente', self.gf('django.db.models.fields.IntegerField')()),
            ('genero', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('formacion', ['EvaluacionCurso'])


    def backwards(self, orm):
        # Deleting model 'EvaluacionCurso'
        db.delete_table('formacion_evaluacioncurso')


    models = {
        'formacion.actividadeventoformacion': {
            'Meta': {'object_name': 'ActividadEventoFormacion'},
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
            'primaria_year': ('django.db.models.fields.IntegerField', [], {'default': '4'}),
            'submodulo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sistema.SubModulo']"})
        },
        'formacion.evaluacioncurso': {
            'Meta': {'object_name': 'EvaluacionCurso'},
            'calidad_contenido': ('django.db.models.fields.IntegerField', [], {}),
            'calificacion_docente': ('django.db.models.fields.IntegerField', [], {}),
            'curso': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['formacion.Curso']", 'unique': 'True'}),
            'genero': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'metodologia': ('django.db.models.fields.IntegerField', [], {})
        },
        'formacion.eventocolectivoformacion': {
            'Meta': {'object_name': 'EventoColectivoFormacion'},
            'actividad': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['formacion.ActividadEventoFormacion']"}),
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
            'sensibilizacion': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'titulo': ('django.db.models.fields.CharField', [], {'max_length': '200'})
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