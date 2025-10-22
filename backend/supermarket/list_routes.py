"""
Script pour afficher toutes les URLs disponibles dans le projet Django.
Usage: python manage.py show_urls (nécessite django-extensions)
Ou: python list_routes.py
"""

import sys
import os
from django.core.management import setup_environ

# Ajouter le chemin du projet au PYTHONPATH
# sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Méthode alternative sans django-extensions
def show_urls():
    """Affiche toutes les URLs du projet"""
    from django.conf import settings
    from django.urls import get_resolver
    
    print("\n" + "="*80)
    print("LISTE DE TOUTES LES ROUTES DE L'API")
    print("="*80 + "\n")
    
    urlconf = __import__(settings.ROOT_URLCONF, {}, {}, [''])
    
    def show_urls_recursive(urlpatterns, prefix=''):
        for pattern in urlpatterns:
            if hasattr(pattern, 'url_patterns'):
                # C'est un include()
                new_prefix = prefix + str(pattern.pattern)
                show_urls_recursive(pattern.url_patterns, new_prefix)
            else:
                # C'est un path/url simple
                full_url = prefix + str(pattern.pattern)
                name = pattern.name if hasattr(pattern, 'name') else ''
                
                # Obtenir la vue
                if hasattr(pattern, 'callback'):
                    view = pattern.callback
                    if hasattr(view, 'cls'):
                        view_name = f"{view.cls.__module__}.{view.cls.__name__}"
                    elif hasattr(view, '__name__'):
                        view_name = f"{view.__module__}.{view.__name__}"
                    else:
                        view_name = str(view)
                else:
                    view_name = "Unknown"
                
                print(f"URL: /{full_url}")
                if name:
                    print(f"  Name: {name}")
                print(f"  View: {view_name}")
                print()
    
    try:
        show_urls_recursive(urlconf.urlpatterns)
    except Exception as e:
        print(f"Erreur: {e}")
        print("\nVeuillez installer django-extensions pour une meilleure visualisation:")
        print("  pip install django-extensions")
        print("  python manage.py show_urls")


if __name__ == "__main__":
    # Configuration de Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'supermarket.settings')
    
    import django
    django.setup()
    
    show_urls()
