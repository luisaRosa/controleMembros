# coding=utf-8

from django.db import models
from localflavor.br.models import *
from datetime import date
from django import forms
import datetime

# Create your models here.

class CargoEclesiastico(models.Model):

	class Meta:
		verbose_name = 'Cargo Eclesiástico'
		verbose_name_plural = 'Cargos Eclesiásticos'

	cargo = models.CharField('Cargo', max_length=45, help_text='Obrigatório. 45 caracteres ou menos.')

	def __str__(self):
		return self.cargo

class Congregacao(models.Model):

	class Meta:
		verbose_name = 'Congregação'
		verbose_name_plural = 'Congregações'

	nome = models.CharField('Nome', max_length=100)
	setor = models.IntegerField('Setor')

	def __str__(self):
		return self.nome


class Membro(models.Model):


	class Meta:
		ordering = ['matricula']

	STATUS_CHOICES = (('A', 'Ativo'),('I', 'Inativo'),)
	SEXO_CHOICES = (('M', 'Masculino'),('F', 'Feminino'),)

	ESTADO_CIVIL_CHOICES = (
        ('S', u'Solteiro(a)'),
        ('C', u'Casado(a)'),
        ('V', u'Viúvo(a)'),
        ('D', u'Divorciado(a)'),
    )

	d  = date.today() # pega a data de hj
	data =  "%s/%s/%s"%(str(d.day), str(d.month), str(d.year))



	status = models.CharField('Status', max_length=5, choices=STATUS_CHOICES, default='A')
	foto = models.ImageField('Foto', default='genome.png')
	matricula= models.BigIntegerField('Matrícula', unique=True )
	data_cadastro = models.DateField('Data de Cadastro',max_length=10, default=d)
	congregacao = models.ForeignKey( Congregacao, on_delete=models.CASCADE)
	cargo = models.ForeignKey(CargoEclesiastico, on_delete=models.CASCADE)

	# Dados pessoais
	nome = models.CharField('Nome', max_length=100)
	sexo = models.CharField('Sexo', max_length=5, choices=SEXO_CHOICES, default='M')
	data_nascimento = models.DateField('Data de Nascimento')
	estado_civil = models.CharField('Estado Civil', max_length=5, choices=ESTADO_CIVIL_CHOICES, default='S')
	conjuge = models.CharField('Cônjuge', max_length=100, blank=True)
	identidade = models.BigIntegerField('Identidade' )
	orgao_emissor = models.CharField('Orgão Emissor', max_length=6)
	cpf = models.BigIntegerField('CPF')
	profissao = models.CharField('Profissão', max_length=15, default="Estudante")
	naturalidade = models.CharField('Naturalidade', max_length=15, default="Rio de Janeiro")
	nacionalidade = models.CharField('Nacionalidade', max_length=15, default='Brasileiro(a)')

	# Contato
	telefone = models.BigIntegerField('Telefone')
	email = models.EmailField('Email', blank=True)

	#endereco
	descricao = models.CharField('Endereço', max_length=100)
	complemento = models.CharField('Complemento', max_length=50)
	bairro =  models.CharField('Bairro', max_length=30, default="Tijuca")
	cidade = models.CharField('Cidade', max_length=30, default="Rio de Janeiro")
	estado = BRStateField(default="RJ")
	cep = models.BigIntegerField('CEP')

	def __str__(self):
		return self.nome

	def ative_members():
		if self.status =='A':
			return True


		#actions = (('ative_members',  	('Membros Ativos')),)






class Endereco(models.Model):

	class Meta:
		verbose_name = 'Endereço'
		verbose_name_plural = 'Endereços'

	membro = models.ForeignKey(Membro, on_delete=models.CASCADE)
	cep = models.BigIntegerField('CEP')
	endereco = models.CharField('Descrição', max_length=100)
	complemento = models.CharField('Complemento', max_length=50)
	cidade = models.CharField('Cidade', max_length=50)
	estado = BRStateField()

	def __str__(self):
		return self.endereco

class Historico(models.Model):

	class Meta:
		verbose_name = 'Histórico'

	membro = models.ForeignKey(Membro, on_delete=models.CASCADE)
	data_batismo = models.DateField('Data de batismo')

	def data_batismo_(self):
		return self.data_batismo
	data_batismo.short_description = 'Data de batismo'

	def __str__(self):
		return self.membro.nome
