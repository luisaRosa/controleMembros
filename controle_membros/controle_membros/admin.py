from django.contrib import admin
from django.urls import path
from django.template.response import TemplateResponse


class MyAdminSite(admin.AdminSite):

   def get_urls(self):
         print("oi")
         from django.conf.urls import url
         urls = admin.AdminSite.get_urls(self)
         urls += [
            path('relatorios/', admin.AdminSite.admin_view(self, self.relatorios))
         ]
         return urls

   def relatorios(self, request):
        context = dict(
           # Include common variables for rendering the admin template.
           admin.AdminSite.each_context(self, request),
           # Anything else you want in the context...

        )
        return TemplateResponse(request, "../templates/admin/reports.html", context)
