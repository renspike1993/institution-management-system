from django.apps import AppConfig
class App2Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.app2'
    verbose_name = "School Library System"  # ✅ ADMIN DISPLAY 