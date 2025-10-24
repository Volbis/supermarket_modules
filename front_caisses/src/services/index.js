/**
 * Point d'entrée centralisé pour tous les services API du module caisses
 * 
 * Usage:
 * import { transactionsAPI, paymentsAPI, promotionsAPI } from '@/services';
 * 
 * Ou:
 * import services from '@/services';
 * services.transactionsAPI.getAllTransactions();
 */

import transactionsAPI from './transactions';
import paymentsAPI from './payments';
import promotionsAPI from './promotions';
import loyaltyAPI from './loyalty';
import reportsAPI from './reports';
import salesAPI from './sales';
import produitsAPI from './produits';

// Export nommé pour imports sélectifs
export {
  transactionsAPI,
  paymentsAPI,
  promotionsAPI,
  loyaltyAPI,
  reportsAPI,
  salesAPI,
  produitsAPI
};

// Export par défaut pour import global
export default {
  transactionsAPI,
  paymentsAPI,
  promotionsAPI,
  loyaltyAPI,
  reportsAPI,
  salesAPI,
  produitsAPI
};
