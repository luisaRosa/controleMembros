# coding=utf-8

from django.db import models
from localflavor.br.models import *
from datetime import date
from django import forms
import datetime
from django.db.models.functions import Extract
from dateutil.relativedelta import relativedelta

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
	setor = models.CharField('Setor',  max_length=2)


	def __str__(self):
		return self.nome


class Membro(models.Model):


	class Meta:
		ordering = ['matricula']

	STATUS_CHOICES = (('A', 'Ativo'),('I', 'Inativo'),)
	SEXO_CHOICES = (('M', 'Masculino'),('F', 'Feminino'),)
	RECEBIMENTO = (('A', ' Por aclamação'),
	('M', 'Com carta de mudança'),
	('B', 'Por Batismo nas Águas'),
	('C', 'Por Convenção'))

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

	#historico
	dataBatismoA = models.DateField(verbose_name='Data de Batismo nas Águas')
	dataBatismoE = models.DateField(verbose_name='Data de Batismo com o Espírito Santo', blank=True)
	recebimento = models.CharField(verbose_name='Recebimento', max_length=5, choices=RECEBIMENTO, default='B')
	addInformacoes = models.TextField(verbose_name='Informações Adicionais', blank=True)

	def __str__(self):
		return self.nome

	def getSituacao():
		return Membro.STATUS_CHOICES

	def idade():
		return date.today() - self.data_nascimento


	def aniversariantes_mes(self, congregacao):

		data  = date.today() # pega a data de hoje

		ativos = Membro.objects.filter(status='A').order_by(Extract('data_nascimento','day'))	
		  
		if int(congregacao) > 0:
			membros = ativos.filter(congregacao_id =congregacao)		
		else:
			membros = ativos			
		
		aniversariantes = []	
    
		for membro in membros:			
			if data.month == membro.data_nascimento.month:
				aniversariantes.append(membro)			
					
		return aniversariantes

	def lista_obreiros(self, select, members_selected=None):

		if members_selected == None:
			membros = Membro.objects.filter(status='A')
		else:
			if select == 0:
				print("aqui123")
				membros = members_selected
			elif select == 1:
				membros = members_selected.filter(status='A')
			else:
				membros = members_selected.filter(status='I')
		obreiros = []

		for membro in membros:
			if membro.cargo.cargo != 'Membro':
				obreiros.append(membro)
		return obreiros

	def getIdade(membros, options):
		
		idades = []
		hoje = date.today()		

		for membro in membros:
			idade = relativedelta(hoje, membro.data_nascimento).years
			print(idade)
			if int(options)==1:				
				if idade<18:
					idades.append(membro)
			elif int(options) == 2:
				if idade>=18 and idade <=24:
					idades.append(membro)
			elif int(options) == 3:
				if idade>=25 and idade <30:
					idades.append(membro)
			elif int(options) == 4:
				if idade>=31 and idade <=60:
					idades.append(membro)
			elif int(options)>60:
				idades.append(membro)
			
		return idades	



	def getMembers(self, cargo, congregacao, idade, situacao):

		members_selected = Membro.objects.all()		

		if int(congregacao) == int(cargo) == int(idade) == (situacao) == 0:			
			return members_selected
		elif int(congregacao)>0 and int(cargo)>0 and int(idade)>0 and situacao != 0:
			members_selected =  members_selected.filter(congregacao_id=congregacao, cargo_id=cargo, status=situacao) ## add o filtro de idade
			return Membro.getIdade(members_selected, idade)
		else:
			print(members_selected)
					
			if  int(congregacao)>0 :
				members_selected = members_selected.filter(congregacao_id=congregacao)			
			if  situacao!= '0':
				members_selected = 	members_selected.filter(status=situacao)
			if int(cargo)>0:
				members_selected = members_selected.filter(cargo_id=cargo)
			elif int(cargo) == -1:
				if situacao == '0':
					members_selected = Membro.lista_obreiros(self, 0, members_selected)
				elif situacao == 'A':
					members_selected = Membro.lista_obreiros(self, 1, members_selected)
				else:
					members_selected = Membro.lista_obreiros(self, 2, members_selected)
				
			if int(idade)>0:
				members_selected = Membro.getIdade(members_selected, idade)			
		return members_selected

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
