from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.http import HttpResponse, Http404
from .models import CargoEclesiastico, Membro, Congregacao, Endereco, Historico
from django.contrib.admin import AdminSite
from django.urls import path
from django.conf.urls import url
from django.contrib import admin

# Register your models here.


@admin.register(CargoEclesiastico)
class CargoAdmin(admin.ModelAdmin):
    fieldsets = [("Cadastrar Cargo Eclesiástico", {'fields': ['cargo']})]
    list_filter = ('cargo',)

class StatusFilter(SimpleListFilter):
    title = ('Status')

    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return (
            (None, 'Ativo'),
            ('I', 'Inativo'),
            ('all', 'All'),
        )

    def choices(self, cl):
        for lookup, title in self.lookup_choices:
            yield {
                'selected': self.value() == lookup,
                'query_string': cl.get_query_string({
                    self.parameter_name: lookup,
                }, []),
                'display': title,
            }

    def queryset(self, request, queryset):
        if self.value() == None:
            return queryset.filter(status='A')
        elif self.value() in ('Inativo'):
            return queryset.filter(status=self.value())



@admin.register(Membro)
class MembroAdmin(admin.ModelAdmin):



     fieldsets = [
        ("Cadastrar Membro", {'fields': ['status','matricula','data_cadastro','nome', 'data_nascimento','sexo','estado_civil',
            'conjuge', 'identidade','orgao_emissor','cpf','congregacao','naturalidade','nacionalidade','cargo','email', 'telefone',
                            ], 'classes':['wide', 'extrapretty']})]
     list_filter = (StatusFilter, 'cargo', 'congregacao')
     readonly_fields=('data_cadastro',)
     list_display=('matricula','cargo','nome', 'congregacao','status' )
     search_fields = ('matricula', 'nome')





@admin.register(Endereco)
class EnderecoAdmin(admin.ModelAdmin):
     fieldsets = [
        ("Cadastrar Endereço", {'fields': ['membro','cep','endereco', 'complemento', 'cidade', 'estado']})]

     list_filter = ('membro',)

@admin.register(Congregacao)
class CongregacaoAdmin(admin.ModelAdmin):
     fieldsets = [
        ("Cadastrar Congregação", {'fields': ['nome','setor',]})]

     list_filter = ('nome', 'setor',)

@admin.register(Historico)
class HistoricoAdmin(admin.ModelAdmin):
     fieldsets = [
        ("Cadastrar Histórico", {'fields': ['membro','data_batismo',]})]

     list_filter = ('membro',)
     #list_display = ('data_batismo_', )

class TemplateAdmin(admin.ModelAdmin):
    AdminSite.index_template = '../templates/admin/aca.html'
    change_form_template = '../templates/admin/reports.html'
    

class CustomAdminSite(admin.AdminSite):

    def get_urls(self):
        urls = super(CustomAdminSite, self).get_urls()
        custom_urls = [
            url(r'desired/path$', self.admin_view(self.genReport), name="relatorios"),
        ]
        return urls + custom_urls

    def genReport(request):
        context = dict(
           # Include common variables for rendering the admin template.
           self.admin_site.each_context(request),
        )
        return TemplateResponse(request, "reports.html", context)
