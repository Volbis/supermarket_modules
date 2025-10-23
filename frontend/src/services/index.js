/**
 * Point d'entrée centralisé pour tous les services API
 * Permet d'importer facilement tous les services depuis un seul endroit
 * 
 * Usage:
 * import { categoriesAPI, produitsAPI, fournisseursAPI } from '@/services';
 * 
 * Ou:
 * import services from '@/services';
 * services.categoriesAPI.getAllCategories();
 */

import categoriesAPI from './categories';
import produitsAPI from './produits';
import fournisseursAPI from './fournisseurs';
import stocksAPI from './stocks';
import commandesAPI from './commandes';
import detailsCommandesAPI from './detailsCommandes';
import alertesAPI from './alertes';
import historiqueStockAPI from './historiqueStock';
import responsablesAPI from './responsables';
import historiqueVentesAPI from './historiqueVentes';

// Export nommé pour imports sélectifs
export {
  categoriesAPI,
  produitsAPI,
  fournisseursAPI,
  stocksAPI,
  commandesAPI,
  detailsCommandesAPI,
  alertesAPI,
  historiqueStockAPI,
  responsablesAPI,
  historiqueVentesAPI
};

// Export par défaut pour import global
export default {
  categoriesAPI,
  produitsAPI,
  fournisseursAPI,
  stocksAPI,
  commandesAPI,
  detailsCommandesAPI,
  alertesAPI,
  historiqueStockAPI,
  responsablesAPI,
  historiqueVentesAPI
};
