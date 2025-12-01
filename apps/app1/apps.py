from django.apps import AppConfig
class App1Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.app1'
    verbose_name = "Registrar's Office"  # ✅ ADMIN DISPLAY 