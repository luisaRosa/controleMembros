from django.contrib import admin
from django.urls import path
from django.template.response import TemplateResponse
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from .print import LetterMaker
from .printing import Print
from io import BytesIO
from django.http import HttpResponse  
from controle.models import Congregacao 

class MyAdminSite(admin.AdminSite):

   class Media:
        print("media")
        css = {
        'all': ('admin/icons_change.css',)
         }

   

   def get_urls(self):
         print("oi")
         from django.conf.urls import url
         urls = admin.AdminSite.get_urls(self)
         urls += [
            path('relatorios/', admin.AdminSite.admin_view(self, self.relatorios)),
            path('relatorios/aniversariantes', admin.AdminSite.admin_view(self, self.getAniversariantes), name='aniversariantes'),
             path('relatorios/obreiros', admin.AdminSite.admin_view(self, self.getObreiros), name='obreiros')
         ]
         return urls

   def relatorios(self, request):

            
        context = dict(
           # Include common variables for rendering the admin template.
           admin.AdminSite.each_context(self, request),
           options = Congregacao.objects.all(),   
           # Anything else you want in the context...

        )
        #print(options)
        return TemplateResponse(request, "../templates/admin/reports.html", context)

   def generatePDF(self, request):

       file_name = "Aniversariantes do mes.pdf"
      
       buffer = io.BytesIO()       
       
       pdf = LetterMaker(buffer, file_name, "The MVP", 10)
       pdf.createDocument()       
       pdf.savePDF()

       buffer.seek(io.SEEK_SET)

       return FileResponse(buffer, as_attachment=True, filename='Aniversariantes do mes.pdf')

   def getAniversariantes(self,request):

       # Create the HttpResponse object with the appropriate PDF headers.
       response = HttpResponse(content_type='application/pdf')
       response['Content-Disposition'] = 'attachment; filename="Aniversariantes do Mes.pdf"'

       buffer = BytesIO()
       # Create the PDF object, using the buffer as its "file."
       report = Print(buffer, 'Letter')
       congregacao = request.GET['l1']
       print(congregacao)

       pdf = report.print_anivesariantes(congregacao)

       response.write(pdf)
       return response

   def getObreiros(self, request):

       # Create the HttpResponse object with the appropriate PDF headers.
       response = HttpResponse(content_type='application/pdf')
       response['Content-Disposition'] = 'attachment; filename="Relacao de obreiros.pdf"'

       buffer = BytesIO()
       # Create the PDF object, using the buffer as its "file."
       report = Print(buffer, 'Letter')
       pdf = report.print_obreiros()

       response.write(pdf)
       return response

       
       
