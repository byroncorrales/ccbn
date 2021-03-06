# -*- coding: utf-8 -*-
from django.contrib import admin
from django import forms
from django.forms import CheckboxSelectMultiple
from prevencion.models import InscripcionPrevencionInterna, InscripcionPrevencionExterna
from models import *
from django.contrib.admin.models import LogEntry, DELETION
from django.utils.html import escape
from django.core.urlresolvers import reverse
from django.forms.models import BaseInlineFormSet


class RequiredInlineFormSet(BaseInlineFormSet):
    """
    Generates an inline formset that is required
    encontrado en http://stackoverflow.com/questions/1206903/how-do-i-require-an-inline-in-the-django-admin
    """

    def _construct_form(self, i, **kwargs):
        """
        Override the method to change the form attribute empty_permitted
        """
        form = super(RequiredInlineFormSet, self)._construct_form(i, **kwargs)
        form.empty_permitted = False
        return form

class LogEntryAdmin(admin.ModelAdmin):
    date_hierarchy = 'action_time'
    readonly_fields = LogEntry._meta.get_all_field_names()
    list_filter = [
        'user',
        'content_type',
        'action_flag'
    ]

    search_fields = [
        'object_repr',
        'change_message'
    ]


    list_display = [
        'action_time',
        'user',
        'content_type',
        'object_link',
        'action_flag',
        'change_message',
    ]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser and request.method != 'POST'

    def has_delete_permission(self, request, obj=None):
        return False

    def object_link(self, obj):
        if obj.action_flag == DELETION:
            link = escape(obj.object_repr)
        else:
            ct = obj.content_type
            link = u'<a href="%s">%s</a>' % (
                reverse('admin:%s_%s_change' % (ct.app_label, ct.model), args=[obj.object_id]),
                escape(obj.object_repr),
            )
        return link
    object_link.allow_tags = True
    object_link.admin_order_field = 'object_repr'
    object_link.short_description = u'Objetos'

admin.site.register(LogEntry, LogEntryAdmin)

class RelacionInline(admin.TabularInline):
    model = Relacion
    fk_name = 'owner'
    extra = 1
    verbose_name_plural = u'Personas de su hogar que estén en CCBN'

class ModuloPersonaInline(admin.StackedInline):
    meh = 'redirect_indicator'
    model = ModuloPersona
    verbose_name_plural = u'Programas a los que pertenece'
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        field = super(ModuloPersonaInline, self).formfield_for_manytomany(db_field, request, **kwargs)
        
        # check if superuser
        if request.user.is_superuser:
            return field

        if not request.user.has_perm('sistema.%s' % db_field.name):
            field.widget.attrs = {'disabled': 'disabled'}

        return field

# Inline para registro en Biblioteca
class RegistroBibliotecaInline(admin.StackedInline):
    model = RegistroBiblioteca
    extra = 1
    max_num = 1
    formset = RequiredInlineFormSet
    verbose_name_plural = u'Registro en Biblioteca'

# Formacion Basica Inline
class FormacionBasicaInline(admin.TabularInline):
    model = InscripcionCurso
    fields = (('curso', 'becado', 'fecha'),)
    extra = 1
    verbose_name_plural = u'Educación Básica'

    def queryset(self, request):
        # override para mostrar solos los modulos adecuados
        queryset = super(FormacionBasicaInline, self).queryset(request)\
                    .filter(curso__submodulo__code='educacionbasica')

        if not self.has_change_permission(request):
            queryset = queryset.none()
        return queryset 

    def formfield_for_dbfield(self, db_field, **kwargs):
        # override para sobreescribir el form field y agregar la clase CSS chozen
        # para agregar el filtro en los combos
        if db_field.name == 'curso':
            return forms.ModelChoiceField(label='Seleccionar Curso', queryset=Curso.objects.filter(submodulo__code='educacionbasica'), 
                                          widget=forms.Select(attrs={'class': 'chozen'}))
        return super(FormacionBasicaInline, self).formfield_for_dbfield(db_field, **kwargs)

# Formacion Tecnica Vocacional
class FormacionVocacionalInline(admin.TabularInline):
    model = InscripcionCurso
    verbose_name_plural = u'Formación Técnica Vocacional'
    extra = 1    
    fields = (('curso', 'becado', 'fecha'), )

    def queryset(self, request):
        # override para solo mostrar los registros de este Inline Formacion Tecnica Vocacional
        queryset = super(FormacionVocacionalInline, self).queryset(request)\
                    .filter(curso__submodulo__code='formacionvocacional')

        if not self.has_change_permission(request):
            queryset = queryset.none()
        return queryset

    def formfield_for_dbfield(self, db_field, **kwargs):
        # override para sobreescribir el form field y agregar la clase CSS chozen
        # para agregar el filtro en los combos
        if db_field.name == 'curso':
            return forms.ModelChoiceField(label=u'Seleccionar Curso', queryset=Curso.objects.filter(submodulo__code='formacionvocacional'), 
                                          widget=forms.Select(attrs={'class': 'chozen'}))
        return super(FormacionVocacionalInline, self).formfield_for_dbfield(db_field, **kwargs)

# Formacion Artistica
class FormacionArtisticaInline(admin.TabularInline):
    model = InscripcionCurso
    verbose_name_plural = u'Formación Artística'
    extra = 1    
    fields = (('curso', 'becado', 'fecha'), )

    def queryset(self, request):
        # override para solo mostrar los registros de este Inline Formacion Tecnica Vocacional
        queryset = super(FormacionArtisticaInline, self).queryset(request)\
                    .filter(curso__submodulo__code='formacionartistica')

        if not self.has_change_permission(request):
            queryset = queryset.none()
        return queryset 

    def formfield_for_dbfield(self, db_field, **kwargs):
        # override para sobreescribir el form field y agregar la clase CSS chozen
        # para agregar el filtro en los combos
        if db_field.name == 'curso':
            return forms.ModelChoiceField(label=u'Seleccionar Curso', queryset=Curso.objects.filter(submodulo__code='formacionartistica'), 
                                          widget=forms.Select(attrs={'class': 'chozen'}))
        return super(FormacionArtisticaInline, self).formfield_for_dbfield(db_field, **kwargs)

# Inlines de Registro de Becas
class RegistroBecaPrimariaInline(admin.TabularInline):
    model = RegistroBecaPrimaria
    extra = 1
    exclude = ('tutoria', 'rendimiento_academico', 'recibio_suplemento', 
               'recibio_atencion_psicologica', 'mejoro_habilidades', 'reconoce_capacidad', 'perc_derecho')
    verbose_name_plural = u'Registro Beca de Primaria'

class RegistroBecaSecundariaInline(admin.TabularInline):
    model = RegistroBecaSecundaria
    extra = 1
    exclude = ('servicio_social', 'esp_propos', 'promotor', 'solidario_famila', 
               'solidario_centro','solidario_comunidad', 'solidario_sociedad')
    verbose_name_plural = u'Registro Beca de Secundaria'

class RegistroBecaUniversitariaInline(admin.TabularInline):
    model = RegistroBecaUniversitaria
    extra = 1
    exclude = ('servicio_social', 'esp_propos', 'promotor', 'solidario_famila', 
               'solidario_centro','solidario_comunidad', 'solidario_sociedad')
    verbose_name_plural = u'Registro Beca Universitaria'

class RegistroFamiliaBecadoInline(admin.TabularInline):
    model = RegistroFamiliaBecado
    extra = 1
    fields = ('persona', 'fecha', 'beca')
    verbose_name_plural = u'Familia de Becado'

# Inlines de registro en grupos musicales
class BasePromocionInline(admin.TabularInline):
    fields = ['fecha', 'grupo']
    model = InscripcionGrupo
    extra = 1
    # key_code = submodulo code ejm: grupomusica, grupoteatro
    # default grupomusica
    key_code = 'grupomusica' 

    def queryset(self, request):
        # override para solo mostrar los registros de Grupo Artistico de Musica
        queryset = super(BasePromocionInline, self).queryset(request)\
                    .filter(grupo__submodulo__code=self.key_code)

        if not self.has_change_permission(request):
            queryset = queryset.none()
        return queryset

    def formfield_for_dbfield(self, db_field, **kwargs):
        # override para sobreescribir el form field y agregar la clase CSS chozen
        # para agregar el filtro en los combos
        if db_field.name == 'grupo':
            return forms.ModelChoiceField(
                label=u'Seleccionar Grupo', 
                queryset=Grupo.objects.filter(submodulo__code=self.key_code), 
                widget=forms.Select(attrs={'class': 'chozen'})
            )
        return super(BasePromocionInline, self).formfield_for_dbfield(db_field, **kwargs)

class RegistroMusicaInline(BasePromocionInline):
    key_code = 'grupomusica'
    verbose_name_plural = u'Grupo Musica'

class RegistroTeatroInline(BasePromocionInline):
    key_code = 'grupoteatro'
    verbose_name_plural = u'Grupo de teatro'

class RegistroDanzaInline(BasePromocionInline):
    key_code = 'grupodanza'
    verbose_name_plural = u'Grupo de danza'

class RegistroCoroInline(BasePromocionInline):
    key_code = 'grupocoro'
    verbose_name_plural = u'Grupo de coro'

class RegistroPinturaInline(BasePromocionInline):
    key_code = 'grupopintura'
    verbose_name_plural = u'Grupo de pintura'

# Programa VBG Interna
class InscripcionPVBGInternaInline(admin.TabularInline):
    model = InscripcionPrevencionInterna
    extra = 1
    exclude = ('asistencia', 'razon_no_asistir', 'calificacion', 'mejora_autoestima', 
               'nivel_conocimiento', 'calidad_contenido', 'metodologia', 'empoderamiento')

class InscripcionPVBGExternaInline(admin.TabularInline):
    model = InscripcionPrevencionExterna
    extra = 1
    fields = ('fecha', 'persona', 'pvbg_externa')

class PersonaAdmin(admin.ModelAdmin):
    list_filter = ['barrio','ciudad']
    search_fields = ['primer_nombre','segundo_nombre','primer_apellido','segundo_apellido','id']
    list_display = ['individuos','fecha_nacimiento','sexo','municipio', 'ciudad','barrio']
    add_form_template = 'admin/registro/add_form_template.html'
    fieldsets = [
        ('Datos personales', {'fields': [('primer_nombre', 'segundo_nombre'), ('primer_apellido', 'segundo_apellido'), 
                                        ('sexo', 'fecha_nacimiento'), ('cedula')]}),
        (u'Relación con CCBN', {'fields': [('docente', 'personal', 'alumno', 'visitante','acompanante'), ('becado', 'promotor', 'beneficiario', 'integrante'),]}),
        ('Ubicacion', {'fields': [('municipio', 'ciudad'), ('barrio'), 'direccion', ('telefono', 'celular')]}),
        (u'Información Académica', {'fields': [('nivel_academico', 'nivel_estudio'), 'centro_actual']}),
        ('Datos del Hogar', {'fields': [('tiene_hijos', 'oficio'), 'con_quien_vive', 'tipo_familia',]}),
        ('Jefe de Familia', {'fields': [('jefe_familia', 'j_oficio'), ('j_primer_nombre', 'j_segundo_nombre'), 
                                        ('j_primer_apellido', 'j_segundo_apellido')],})
                                                                                     
    ]

    inlines = [RelacionInline, ModuloPersonaInline, FormacionBasicaInline, 
            FormacionVocacionalInline, FormacionArtisticaInline]

    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }
    readonly_fields = ('codigo', )



    def response_add(self, request, obj):
        return super(PersonaAdmin, self).response_add(request, obj, '../%s/#shva')

    def add_view(self, request):
        self.inlines=[RelacionInline, ModuloPersonaInline]
        return super(PersonaAdmin, self).add_view(request)

    def change_view(self, request, obj_id):
        inlines = []
        self.inlines = [RelacionInline, ModuloPersonaInline]        
        try:
            modulos = Persona.objects.get(id=obj_id).modulopersona
            
            # agregando inlines del modulo biblioteca
            for obj in modulos.biblioteca.all().exclude(inline__exact=''):
                inlines.append(obj.inline)
            # agregando inlines del modulo de formacion        
            for obj in modulos.formacion.all().exclude(inline__exact=''):
                inlines.append(obj.inline)
            # agregando inlines del modulo de atencion integrals
            for obj in modulos.atencion_integral.all().exclude(inline__exact=''):
                inlines.append(obj.inline)
            # agregando inlines del modulo de promocion artistica
            for obj in modulos.promocion_artistica.all().exclude(inline__exact=''):
                inlines.append(obj.inline)
            # agregando inlines del modulo de prevencion interna
            for obj in modulos.pv_interna.all().exclude(inline__exact=''):
                inlines.append(obj.inline)
            # agregando inlines del modulo de prevencion externa
            for obj in modulos.pv_externa.all().exclude(inline__exact=''):
                inlines.append(obj.inline)

            self.inlines += [eval(inline) for inline in inlines]

        except Exception as e:            
            print e

        return super(PersonaAdmin, self).change_view(request, obj_id)

    class Media:
        css = {
            'screen': ('/files/css/admin.css', '/files/js/chosen.css'),            
        }
        js= ['http://ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js', 
            '/files/js/chosen.jquery.min.js', '/files/js/admin.js']


admin.site.register(Persona, PersonaAdmin)
admin.site.register(Pariente)
admin.site.register(Relacion)
admin.site.register(Ciudad)
class BarrioAdmin(admin.ModelAdmin):
    list_display = ['barrios']
    search_fields = ('nombre',)

admin.site.register(Barrio, BarrioAdmin)
admin.site.register(Oficio)

class ColegioAdmin(admin.ModelAdmin):
    list_display = ['escuelas']
    search_fields = ('nombre',)

admin.site.register(Colegio, ColegioAdmin)
