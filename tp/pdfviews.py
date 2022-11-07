from django.shortcuts import render, redirect
from .models import Student

from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

def student(request):
 
    return render(request, 'pdf/confirmstudentpdf.html')

def student_pdf_generate(request, student_id):
    student = Student.objects.get(id=student_id)
    template_path = 'pdf/confirmstudentpdf.html'
    context = {"student":student}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = "filename=" + str(student.matricule) +"_TP.pdf"
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

