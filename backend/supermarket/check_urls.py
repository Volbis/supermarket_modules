#!/usr/bin/env python3
"""
Script pour vérifier la configuration des URLs Django
"""
import os
import sys
import django

# Configuration de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'supermarket.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

django.setup()

from django.conf import settings
from django.urls import get_resolver
from django.urls.resolvers import URLPattern, URLResolver

def list_urls(urlpatterns, prefix='', depth=0):
    """Liste récursivement toutes les URLs"""
    for pattern in urlpatterns:
        if isinstance(pattern, URLResolver):
            # C'est un include()
            new_prefix = prefix + str(pattern.pattern)
            print(f"{'  ' * depth}📁 {new_prefix}")
            list_urls(pattern.url_patterns, new_prefix, depth + 1)
        elif isinstance(pattern, URLPattern):
            # C'est un path/url simple
            full_url = prefix + str(pattern.pattern)
            name = pattern.name if pattern.name else "no-name"
            print(f"{'  ' * depth}🔗 {full_url} [{name}]")

print("\n" + "="*80)
print("LISTE COMPLÈTE DES URLS DJANGO")
print("="*80 + "\n")

try:
    resolver = get_resolver()
    list_urls(resolver.url_patterns)
    print("\n" + "="*80)
    print("✅ URLs chargées avec succès!")
    print("="*80 + "\n")
except Exception as e:
    print(f"\n❌ ERREUR lors du chargement des URLs:")
    print(f"{type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
