/**
 * Composable pour gérer le cache des données
 * 
 * Permet de:
 * - Mettre en cache les réponses API pour éviter des requêtes inutiles
 * - Invalider le cache manuellement ou automatiquement
 * - Vérifier l'âge du cache
 * - Forcer le refresh des données
 * 
 * Usage:
 * const { loadWithCache, invalidateCache, cacheStatus } = useDataCache();
 * 
 * const data = await loadWithCache('products', async () => {
 *   return await productsAPI.getAllProducts();
 * });
 */

import { reactive } from 'vue';

// Store centralisé du cache (partagé entre toutes les instances du composable)
const cacheStore = reactive({});

// Durée de vie par défaut du cache en millisecondes (5 minutes)
const DEFAULT_CACHE_TTL = 5 * 60 * 1000;

export function useDataCache() {
  /**
   * Charge des données avec mise en cache
   * @param {string} key - Clé unique pour identifier le cache
   * @param {Function} fetchFn - Fonction async qui retourne les données à mettre en cache
   * @param {boolean} forceRefresh - Force le rechargement même si le cache est valide
   * @param {number} ttl - Durée de vie du cache en millisecondes
   * @returns {Promise} Les données (depuis le cache ou fraîchement chargées)
   */
  async function loadWithCache(key, fetchFn, forceRefresh = false, ttl = DEFAULT_CACHE_TTL) {
    const now = Date.now();
    
    // Vérifier si on a un cache valide et qu'on ne force pas le refresh
    if (!forceRefresh && cacheStore[key] && (now - cacheStore[key].timestamp) < ttl) {
      console.log(`✅ Cache HIT pour "${key}" (âge: ${Math.floor((now - cacheStore[key].timestamp) / 1000)}s)`);
      return cacheStore[key].data;
    }
    
    // Cache invalide ou forcé: charger les données
    console.log(`🔄 Cache MISS pour "${key}" - Chargement depuis l'API...`);
    
    try {
      const data = await fetchFn();
      
      // Mettre en cache
      cacheStore[key] = {
        data: data,
        timestamp: now
      };
      
      console.log(`💾 Données mises en cache pour "${key}"`);
      return data;
      
    } catch (error) {
      console.error(`❌ Erreur lors du chargement de "${key}":`, error);
      
      // En cas d'erreur, retourner le cache même s'il est expiré (fallback)
      if (cacheStore[key]) {
        console.warn(`⚠️ Utilisation du cache expiré pour "${key}" (fallback)`);
        return cacheStore[key].data;
      }
      
      throw error;
    }
  }
  
  /**
   * Invalide le cache pour une clé donnée
   * @param {string} key - Clé du cache à invalider (ou 'all' pour tout invalider)
   */
  function invalidateCache(key) {
    if (key === 'all') {
      Object.keys(cacheStore).forEach(k => delete cacheStore[k]);
      console.log('🗑️ Tout le cache a été invalidé');
    } else if (cacheStore[key]) {
      delete cacheStore[key];
      console.log(`🗑️ Cache invalidé pour "${key}"`);
    }
  }
  
  /**
   * Retourne le statut du cache pour une clé donnée
   * @param {string} key - Clé du cache à vérifier
   * @returns {Object} Statut du cache (exists, age, isExpired)
   */
  function cacheStatus(key, ttl = DEFAULT_CACHE_TTL) {
    if (!cacheStore[key]) {
      return { exists: false, age: null, isExpired: true };
    }
    
    const now = Date.now();
    const age = now - cacheStore[key].timestamp;
    const isExpired = age > ttl;
    
    return {
      exists: true,
      age: Math.floor(age / 1000), // en secondes
      isExpired: isExpired
    };
  }
  
  /**
   * Pré-charge des données en cache
   * @param {string} key - Clé pour le cache
   * @param {any} data - Données à mettre en cache
   */
  function preloadCache(key, data) {
    cacheStore[key] = {
      data: data,
      timestamp: Date.now()
    };
    console.log(`📥 Données pré-chargées en cache pour "${key}"`);
  }
  
  return {
    loadWithCache,
    invalidateCache,
    cacheStatus,
    preloadCache
  };
}
