from django.contrib import admin
from django.db import models
from django.contrib.admin import SimpleListFilter
from django.http import HttpResponse, Http404
from .models import CargoEclesiastico, Membro, Congregacao, Endereco, Historico
from django.contrib.admin import AdminSite

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
            (None, 'Ativos'),
            ('I', 'Inativos'),
            ('all', 'Todos'),
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

    formfield_overrides = {
     models.DateField: {'input_formats': ('%d/%m/%Y',)},
   }


    date_hierarchy = 'data_cadastro'

    fieldsets = [
        ("Dados Cadastrais", {'fields': ['matricula', 'status','data_cadastro' ]}),
        ("Dados Pessoais",{'fields':[('nome', 'sexo'), 'data_nascimento', 'cpf', ('identidade', 'orgao_emissor'),
       ( 'estado_civil', 'conjuge'), ('naturalidade', 'nacionalidade')]}),
        ("Dados Eclesiásticos", {'fields':['congregacao', 'cargo']}),
        ("Dados para Contato", {'fields':['telefone', 'email']}),
        ("Dados de Endereço", {'fields':[('descricao', 'complemento'), ('bairro', 'cidade', 'estado'), 'cep']})

        ]


   # 'nome', 'data_nascimento','sexo','estado_civil', 'classes':['wide', 'extrapretty']
   #         'conjuge', ('identidade','orgao_emissor'),'cpf',('naturalidade','nacionalidade'),('congregacao','cargo'),'email', 'telefone',
    list_filter = (StatusFilter, 'cargo', 'congregacao')
    list_select_related = ('cargo', 'congregacao')
    readonly_fields=('data_cadastro',)
    list_display=('matricula','nome', 'cargo', 'congregacao','status' )
    list_display_links = ('matricula','nome',)
    search_fields = ('matricula', 'nome')
    radio_fields = {"sexo": admin.HORIZONTAL, "estado_civil":admin.HORIZONTAL, "status":admin.HORIZONTAL}
    autocomplete_fields = ['congregacao']



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
     search_fields = ['nome']

@admin.register(Historico)
class HistoricoAdmin(admin.ModelAdmin):
     fieldsets = [
        ("Cadastrar Histórico", {'fields': ['membro','data_batismo',]})]

     list_filter = ('membro',)
