from .models import  SiteInfo, Service
from django.contrib.auth.models import AnonymousUser

def site_info(request):
    """
    Fournit les informations globales du site à tous les templates.
    """
    site = SiteInfo.objects.first()  # On suppose un seul enregistrement
    return {
        'site_info': site
    }

def services_pro(request):
    services = Service.objects.all()

    return {
        'services':services
    }