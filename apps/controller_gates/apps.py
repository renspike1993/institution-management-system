from django.apps import AppConfig


class ControllerGatesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.controller_gates'   # ✅ THIS MUST MATCH INSTALLED_APPS
    verbose_name = "Controller Gates"