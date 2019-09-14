from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from controle.models import Membro
from reportlab.lib.units import inch, mm
from reportlab.pdfgen import canvas
import os.path
from reportlab.lib import colors
from django.contrib import messages

class Print:
    def __init__(self, buffer, pagesize):
        
        self.buffer = buffer
        if pagesize == 'A4':
            self.pagesize = A4
        elif pagesize == 'Letter':
            self.pagesize = letter
        self.width, self.height = self.pagesize

    @staticmethod
    def _header_footer(canvas, doc):
        # Save the state of our canvas so we can draw on it
        canvas.saveState()
        styles = getSampleStyleSheet()
 
        # Header

        header = Paragraph('Igreja Evangélica Assembleia de Deus Tijuca Gloriosa ', styles['Normal'])       

        #data = [[logo, p]]
        #header = Table(data, colWidths=2*inch)
        #header.setStyle([("VALIGN", (1,1), (1,1), "TOP")])
        header.wrap(doc.width, doc.topMargin)
        w, h = header.wrap(doc.width, doc.topMargin)
        
        header.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - h)
         
        
        #header.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - h)
 
        # Footer
        footer = Paragraph('This is a multi-line footer.  It goes on every page.   ' * 5, styles['Normal'])
        w, h = footer.wrap(doc.width, doc.bottomMargin)
        footer.drawOn(canvas, doc.leftMargin, h)
 
        # Release the canvas
        canvas.restoreState()
    
    def print_anivesariantes(self, congregacao):
        buffer = self.buffer
        doc = SimpleDocTemplate(buffer,
                                rightMargin=inch/4,
                                leftMargin=inch/4,
                                topMargin=inch/4,
                                bottomMargin=inch/4,
                                pagesize=self.pagesize)
        # Our container for 'Flowable' objects
        elements = []
        # A large collection of style sheets pre-made for us
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='centered', alignment=TA_CENTER))

        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'header.png')
        logo = Image(path)
        logo.drawHeight, logo.drawWidth = 1.2*inch, 6.7*inch

        p = Paragraph("",styles['Normal'])

        data= [[logo,p]]

        chart_style = TableStyle([('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                          ('VALIGN', (0, 0), (-1, -1), 'CENTER')])
      
        header=Table(data)
        #header.setStyle(TableStyle(colWidths=[1.3 * inch, 1.3 * inch],
                     #rowHeights=[1.5 * inch], style=chart_style))
       
        elements.append(header)



        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.
        aniversariantes = Membro.aniversariantes_mes(self, congregacao)
        elements.append(Paragraph('Aniversariantes do Mês', styles['Heading2']))
        elements.append(Paragraph(" ", styles['Normal']))
        tabela = []
        id_=1
        for i, membro in enumerate(aniversariantes):
            d = membro.data_nascimento
            data =  "%s/%s/%s"%(str(d.day), str(d.month), str(d.year))
            tabela.append([str(id_)+"                             ", membro.nome+"                                                                                          ", data])
            id_+=1
            #elements.append(Paragraph(str(membro.matricula) +"   -    "+ membro.nome+ "     "+ data, styles['Normal']))
      
            T = Table(tabela)
            T.setStyle(TableStyle(colWidths=[4.3 * inch, 4.3 * inch, 4.3 * inch],
                     rowHeights=[5.5 * inch], style=chart_style))
            elements.append(T)
        
        

        doc.build(elements,canvasmaker=NumberedCanvas)

        # Get the value of the BytesIO buffer and write it to the response.
        pdf = buffer.getvalue()
        buffer.close()


        return pdf


    def print_obreiros(self):
            buffer = self.buffer
            doc = SimpleDocTemplate(buffer,
                                    rightMargin=inch/4,
                                    leftMargin=inch/4,
                                    topMargin=inch/4,
                                    bottomMargin=inch/4,
                                    pagesize=self.pagesize)
            # Our container for 'Flowable' objects
            elements = []
            # A large collection of style sheets pre-made for us
            styles = getSampleStyleSheet()
            styles.add(ParagraphStyle(name='centered', alignment=TA_CENTER))

            path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'header.png')
            logo = Image(path)
            logo.drawHeight, logo.drawWidth = 1.2*inch, 6.7*inch

            p = Paragraph("",styles['Normal'])

            data= [[logo,p]]

            chart_style = TableStyle([('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                            ('VALIGN', (0, 0), (-1, -1), 'CENTER')])
        
            header=Table(data)
            #header.setStyle(TableStyle(colWidths=[1.3 * inch, 1.3 * inch],
                        #rowHeights=[1.5 * inch], style=chart_style))
        
            elements.append(header)



            # Draw things on the PDF. Here's where the PDF generation happens.
            # See the ReportLab documentation for the full list of functionality.
            obreiros = Membro.lista_obreiros(self,1)
            elements.append(Paragraph('Relação de Obreiros', styles['Heading2']))
            elements.append(Paragraph(" ", styles['Normal']))
            tabela = []
        
            for i, membro in enumerate(obreiros):           
                tabela.append([str(i+1)+"         " , membro.cargo.cargo, membro.nome, membro.congregacao.nome,"   ________________________________________________"])            
                #elements.append(Paragraph(str(membro.matricula) +"   -    "+ membro.nome+ "     "+ data, styles['Normal']))
            
            T = Table(tabela)
            T.setStyle(TableStyle(colWidths=[4.3 * inch, 4.3 * inch],
                        rowHeights=[5.5 * inch], style=chart_style))
            elements.append(T)

            doc.build(elements,canvasmaker=NumberedCanvas)

            # Get the value of the BytesIO buffer and write it to the response.
            pdf = buffer.getvalue()
            buffer.close()

            return pdf


    def print_personalizados(self, titulo, campos, filtros):

            buffer = self.buffer
            doc = SimpleDocTemplate(buffer,
                                    rightMargin=inch/4,
                                    leftMargin=inch/4,
                                    topMargin=inch/4,
                                    bottomMargin=inch/4,
                                    pagesize=self.pagesize)

            # Our container for 'Flowable' objects
            elements = []
            # A large collection of style sheets pre-made for us
            styles = getSampleStyleSheet()
            styles.add(ParagraphStyle(name='centered', alignment=TA_CENTER))

            path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'header.png')
            logo = Image(path)
            logo.drawHeight, logo.drawWidth = 1.2*inch, 6.7*inch

            p = Paragraph("",styles['Normal'])

            data= [[logo,p]]

            chart_style = TableStyle([('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                            ('VALIGN', (0, 0), (-1, -1), 'CENTER')])
        
            header=Table(data)
            #header.setStyle(TableStyle(colWidths=[1.3 * inch, 1.3 * inch],
                        #rowHeights=[1.5 * inch], style=chart_style))
        
            elements.append(header)            
           
            elements.append(Paragraph(titulo, styles['Heading2']))
            elements.append(Paragraph(" ", styles['Normal']))

            membros = Membro.getMembers(self, filtros[0], filtros[1], filtros[2], filtros[3])                      

            tabela = []

            caption = []

            caption.append("Número")
            caption.append("  ")

            for c in campos:
                caption.append(c) 
                caption.append("  ")
            tabela.append(caption)

            for i, membro in enumerate(membros):
                 line = []
                 line.append(str(i+1))   
                 line.append("  ")
                 for c in campos:                   
                    line.append(getattr(membro, c))
                    line.append("  ")

                 tabela.append(line)            
                #elements.append(Paragraph(str(membro.matricula) +"   -    "+ membro.nome+ "     "+ data, styles['Normal']))
            
            T = Table(tabela)
            T.setStyle(TableStyle(colWidths=[4.3 * inch, 4.3 * inch],
                        rowHeights=[5.5 * inch], style=chart_style))
            elements.append(T)
        
            doc.build(elements,canvasmaker=NumberedCanvas)

            # Get the value of the BytesIO buffer and write it to the response.
            pdf = buffer.getvalue()
            buffer.close()

            return pdf



class NumberedCanvas(canvas.Canvas):

    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []
 
    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()
  
    def save(self):
        """add page info to each page (page x of y)"""
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)
 
    def draw_page_number(self, page_count):
        # Change the position of this to wherever you want the page number to be
        self.drawRightString(211 * mm, 15 * mm + (0.2 * inch),
                             "Página %d de %d" % (self._pageNumber, page_count))
