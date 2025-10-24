/**
 * Composable pour gérer le cache global des données
 * Partagé entre toutes les pages Vue
 */

import { ref, computed } from 'vue';

// État global partagé (singleton)
const globalCache = ref({
  ventes: { data: null, timestamp: null, ttl: 300000 }, // 5 minutes (données historiques, changent peu)
  commandes: { data: null, timestamp: null, ttl: 180000 }, // 3 minutes (modérément dynamique)
  alertes: { data: null, timestamp: null, ttl: 120000 }, // 2 minutes (alertes critiques, mais pas temps réel)
  produits: { data: null, timestamp: null, ttl: 600000 }, // 10 minutes (catalogue stable)
  categories: { data: null, timestamp: null, ttl: 1800000 }, // 30 minutes (très stable)
  fournisseurs: { data: null, timestamp: null, ttl: 900000 }, // 15 minutes (données stables)
  stocks: { data: null, timestamp: null, ttl: 180000 } // 3 minutes (dynamique mais pas critique)
});

export function useDataCache() {
  /**
   * Vérifie si le cache est valide
   */
  const isCacheValid = (cacheKey) => {
    const cache = globalCache.value[cacheKey];
    if (!cache) {
      console.warn(`⚠️ Cache key "${cacheKey}" n'existe pas`);
      return false;
    }
    
    if (!cache.data || !cache.timestamp) return false;
    
    const now = Date.now();
    const age = now - cache.timestamp;
    
    return age < cache.ttl;
  };

  /**
   * Récupère les données du cache
   */
  const getCachedData = (cacheKey) => {
    if (!globalCache.value[cacheKey]) {
      console.warn(`⚠️ Cache key "${cacheKey}" n'existe pas`);
      return null;
    }
    return globalCache.value[cacheKey].data;
  };

  /**
   * Stocke les données dans le cache
   */
  const setCachedData = (cacheKey, data) => {
    if (!globalCache.value[cacheKey]) {
      console.warn(`⚠️ Cache key "${cacheKey}" n'existe pas`);
      return;
    }
    
    globalCache.value[cacheKey].data = data;
    globalCache.value[cacheKey].timestamp = Date.now();
    
    console.log(`✅ Cache mis à jour: ${cacheKey} (${data?.length || 'N/A'} items)`);
  };

  /**
   * Vide le cache (un seul ou tous)
   */
  const clearCache = (cacheKey = null) => {
    if (cacheKey) {
      if (!globalCache.value[cacheKey]) {
        console.warn(`⚠️ Cache key "${cacheKey}" n'existe pas`);
        return;
      }
      globalCache.value[cacheKey].data = null;
      globalCache.value[cacheKey].timestamp = null;
      console.log(`🗑️ Cache vidé: ${cacheKey}`);
    } else {
      // Vider tout le cache
      Object.keys(globalCache.value).forEach(key => {
        globalCache.value[key].data = null;
        globalCache.value[key].timestamp = null;
      });
      console.log('🗑️ Tout le cache a été vidé');
    }
  };

  /**
   * Force le rafraîchissement d'une clé
   */
  const invalidateCache = (cacheKey) => {
    if (!globalCache.value[cacheKey]) {
      console.warn(`⚠️ Cache key "${cacheKey}" n'existe pas`);
      return;
    }
    globalCache.value[cacheKey].timestamp = null;
    console.log(`⚡ Cache invalidé: ${cacheKey}`);
  };

  /**
   * Obtenir l'âge du cache en millisecondes
   */
  const getCacheAge = (cacheKey) => {
    const cache = globalCache.value[cacheKey];
    if (!cache || !cache.timestamp) return null;
    
    return Date.now() - cache.timestamp;
  };

  /**
   * Obtenir le temps restant avant expiration (en secondes)
   */
  const getCacheTimeRemaining = (cacheKey) => {
    const cache = globalCache.value[cacheKey];
    if (!cache || !cache.timestamp) return 0;
    
    const age = Date.now() - cache.timestamp;
    const remaining = cache.ttl - age;
    
    return remaining > 0 ? Math.ceil(remaining / 1000) : 0;
  };

  /**
   * Computed pour afficher l'état du cache
   */
  const cacheStatus = computed(() => {
    const status = {};
    Object.keys(globalCache.value).forEach(key => {
      const cache = globalCache.value[key];
      status[key] = {
        hasData: !!cache.data,
        isValid: isCacheValid(key),
        age: getCacheAge(key),
        timeRemaining: getCacheTimeRemaining(key),
        itemCount: cache.data?.length || 0
      };
    });
    return status;
  });

  /**
   * Charge les données avec gestion du cache
   */
  const loadWithCache = async (cacheKey, loadFunction, forceRefresh = false) => {
    // Vérifier le cache
    if (!forceRefresh && isCacheValid(cacheKey)) {
      const cachedData = getCachedData(cacheKey);
      console.log(`📦 ${cacheKey} chargé depuis le cache (${cachedData?.length || 0} items)`);
      return cachedData;
    }

    // Charger depuis l'API
    try {
      console.log(`🌐 Chargement ${cacheKey} depuis l'API...`);
      const data = await loadFunction();
      setCachedData(cacheKey, data);
      return data;
    } catch (error) {
      console.error(`❌ Erreur chargement ${cacheKey}:`, error);
      
      // Fallback: utiliser le cache expiré si disponible
      const cachedData = getCachedData(cacheKey);
      if (cachedData) {
        console.log(`⚠️ Utilisation du cache expiré pour ${cacheKey}`);
        return cachedData;
      }
      
      throw error;
    }
  };

  return {
    // État
    globalCache,
    cacheStatus,
    
    // Méthodes
    isCacheValid,
    getCachedData,
    setCachedData,
    clearCache,
    invalidateCache,
    getCacheAge,
    getCacheTimeRemaining,
    loadWithCache
  };
}
