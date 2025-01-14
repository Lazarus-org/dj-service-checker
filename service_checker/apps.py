from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class ServiceCheckerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "service_checker"
    verbose_name = _("Django Service Checker")
