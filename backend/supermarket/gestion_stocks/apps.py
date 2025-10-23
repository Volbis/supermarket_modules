from django.apps import AppConfig


class GestionStocksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gestion_stocks'
    
    def ready(self):
        """Importer les signals au démarrage de l'application."""
        import gestion_stocks.signals