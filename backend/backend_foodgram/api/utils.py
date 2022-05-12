from django.http import HttpResponse
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


def download_page(download_dict):
    pdfmetrics.registerFont(
        TTFont('DejaVuSans', 'DejaVuSans.ttf', 'UTF-8'))
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = (
        'attachment; '
        'filename="shopping_list.pdf"'
    )
    page = canvas.Canvas(response)
    page.setFont('DejaVuSans', size=24)
    page.drawString(200, 800, 'Список покупок')
    page.setFont('DejaVuSans', size=16)
    height = 750
    for i, (name, data) in enumerate(download_dict.items(), 1):
        page.drawString(75, height, (
            f'{i}. {name}: {data["amount"]}, '
            f'{data["measurement_unit"]}'))
        height -= 25
    page.showPage()
    page.save()
    return 