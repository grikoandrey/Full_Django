from django.apps import AppConfig


class MarketConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'market'

    def ready(self):
        from . import signals  # выполнение модуля -> регистрация сигналов
