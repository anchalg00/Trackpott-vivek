import os
from io import BytesIO
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
import xhtml2pdf.pisa as pisa


def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    resources
    """
    # use short variable names
    sUrl = settings.STATIC_URL      # Typically /static/
    sRoot = settings.STATIC_ROOT    # Typically /home/userX/project_static/
    # mUrl = settings.MEDIA_URL       # Typically /static/media/
    # mRoot = settings.MEDIA_ROOT     # Typically /home/userX/project_static/media/

    # convert URIs to absolute system paths
    # if uri.startswith(mUrl):
    #     path = os.path.join(mRoot, uri.replace(mUrl, ""))
    if uri.startswith(sUrl):
        path = os.path.join(sRoot, uri.replace(sUrl, ""))
    else:
        return uri  # handle absolute uri (ie: http://some.tld/foo.png)

    # make sure that file exists
    if not os.path.isfile(path):
            raise Exception(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
    return path

class Render:

    @staticmethod
    def render(path: str, params: dict):
        template = get_template(path)
        html = template.render(params)
        response = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), response, link_callback=link_callback)
        if not pdf.err:
            return HttpResponse(response.getvalue(), content_type='application/pdf')
        else:
            return HttpResponse("Error Rendering PDF", status=400)