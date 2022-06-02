from django.apps import AppConfig

class RestaurantConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'restaurant'

    def ready(self):
        from django.contrib.auth.models import Group
        for group in ['hostess', 'cook', 'server', 'manager']:
            Group.objects.get_or_create(name=group)
