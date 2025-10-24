# 📖 Documentation du Module de Gestion des Caisses

## Table des matières
1. [Architecture](#architecture)
2. [Composants principaux](#composants-principaux)
3. [Services API](#services-api)
4. [Gestion d'état et cache](#gestion-détat-et-cache)
5. [Workflow utilisateur](#workflow-utilisateur)
6. [Intégration avec le backend](#intégration-avec-le-backend)

---

## Architecture

### Vue d'ensemble
Le module suit une architecture en couches :

```
┌─────────────────────────────────────┐
│         Interface Utilisateur       │
│   (Views: PointOfSale, Payment...)  │
└─────────────────┬───────────────────┘
                  │
┌─────────────────▼───────────────────┐
│      Composants & Composables       │
│  (useDataCache, utilitaires...)     │
└─────────────────┬───────────────────┘
                  │
┌─────────────────▼───────────────────┐
│         Services API                │
│ (transactions, payments, sales...)  │
└─────────────────┬───────────────────┘
                  │
┌─────────────────▼───────────────────┐
│      Backend REST API               │
│   (http://localhost:8000/api)       │
└─────────────────────────────────────┘
```

### Principes de conception
- **Composition API** : Utilisation exclusive de la Composition API Vue 3
- **Réutilisabilité** : Composables pour la logique partagée
- **Séparation des responsabilités** : Vues, services, et logique métier séparés
- **Design cohérent** : Respect strict du design system existant

---

## Composants principaux

### 1. App.vue
**Rôle** : Composant racine avec navigation sidebar

**Fonctionnalités** :
- Navigation entre les différentes vues
- Gestion de l'état actif du menu
- Modal de déconnexion
- Rafraîchissement global des données

**Code exemple** :
```javascript
// Appeler la méthode refresh d'une vue
const currentPageComponent = this.$refs.currentPage
if (currentPageComponent?.refreshData) {
  currentPageComponent.refreshData()
}
```

### 2. PointOfSale.vue
**Rôle** : Interface principale de caisse

**Fonctionnalités** :
- Recherche de produits (nom, code-barres)
- Ajout au panier
- Gestion des quantités
- Application de remises
- Suspension de transaction
- Calcul automatique du total (TTC, TVA, remises)

**Workflow** :
1. Rechercher un produit via la barre de recherche
2. Cliquer pour ajouter au panier
3. Modifier les quantités si nécessaire
4. Appliquer une remise optionnelle
5. Procéder au paiement

### 3. Payment.vue (à implémenter)
**Fonctionnalités prévues** :
- Sélection méthode de paiement
- Paiement fractionné
- Calcul de la monnaie
- Validation et confirmation
- Impression ticket

### 4. SalesTracking.vue
**Rôle** : Dashboard de suivi des ventes

**KPIs affichés** :
- CA du jour
- Nombre de transactions
- Panier moyen
- Graphiques de ventes

### 5. Autres vues
- **PromotionsManagement** : Gestion des promotions
- **DailyReports** : Rapports quotidiens
- **CashierClosing** : Clôture de caisse
- **TransactionHistory** : Historique complet
- **Settings** : Paramètres utilisateur

---

## Services API

### Structure d'un service
Chaque service expose des méthodes pour interagir avec le backend :

```javascript
import apiClient from '@/api/api';

export default {
  // GET
  getAllItems() {
    return apiClient.get('/items');
  },
  
  // POST
  createItem(data) {
    return apiClient.post('/items', data);
  },
  
  // PUT
  updateItem(id, data) {
    return apiClient.put(`/items/${id}`, data);
  },
  
  // DELETE
  deleteItem(id) {
    return apiClient.delete(`/items/${id}`);
  }
};
```

### Services disponibles

#### transactionsAPI
```javascript
import { transactionsAPI } from '@/services';

// Récupérer toutes les transactions
const { data } = await transactionsAPI.getAllTransactions();

// Créer une transaction
await transactionsAPI.createTransaction({
  cashier_id: '123',
  items: [...],
  total_amount: 15000
});

// Suspendre une transaction
await transactionsAPI.suspendTransaction(transactionId);
```

#### paymentsAPI
```javascript
import { paymentsAPI } from '@/services';

// Traiter un paiement
await paymentsAPI.processPayment({
  transaction_id: 'TXN-001',
  method: 'cash',
  amount: 15000
});

// Vérifier solde carte cadeau
const balance = await paymentsAPI.checkGiftCardBalance('CARD-123');
```

#### loyaltyAPI
```javascript
import { loyaltyAPI } from '@/services';

// Valider une carte de fidélité
const card = await loyaltyAPI.validateCard('1234567890');

// Ajouter des points
await loyaltyAPI.earnPoints('1234567890', 150, transactionId);
```

---

## Gestion d'état et cache

### useDataCache Composable

Le composable `useDataCache` permet de :
- Mettre en cache les réponses API
- Réduire les appels réseau inutiles
- Améliorer les performances
- Gérer le cycle de vie du cache

**Utilisation** :

```javascript
import { useDataCache } from '@/composables/useDataCache';

export default {
  setup() {
    const { loadWithCache, invalidateCache } = useDataCache();
    return { loadWithCache, invalidateCache };
  },
  
  async mounted() {
    // Charger avec cache (TTL: 5 min par défaut)
    this.products = await this.loadWithCache('products', async () => {
      const response = await produitsAPI.getAllProduits();
      return response.data;
    });
  },
  
  methods: {
    async refreshData() {
      // Invalider le cache et recharger
      this.invalidateCache('products');
      await this.loadProducts(true); // forceRefresh = true
    }
  }
};
```

**Avantages** :
- ✅ Réduction de la latence
- ✅ Diminution de la charge serveur
- ✅ Meilleure expérience utilisateur
- ✅ Mode dégradé en cas d'erreur réseau

---

## Workflow utilisateur

### Scénario complet : Vente avec carte de fidélité

```
┌─────────────────────────────────────────────────────────┐
│ 1. OUVERTURE SESSION CAISSE                            │
│    - Identification caissier                            │
│    - Vérification fond de caisse                        │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│ 2. SCAN/SAISIE PRODUITS                                │
│    - Recherche produit (nom/barcode)                    │
│    - Ajout au panier                                    │
│    - Mise à jour quantités                              │
│    - Affichage sous-total en temps réel                 │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│ 3. SCAN CARTE FIDÉLITÉ                                 │
│    - Validation carte                                   │
│    - Affichage profil client                            │
│    - Application remises automatiques                   │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│ 4. CALCUL AUTOMATIQUE                                  │
│    - Remise seuil (ex: 5% à 100€)                      │
│    - Remise fidélité                                    │
│    - TVA (18%)                                          │
│    - Total TTC                                          │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│ 5. PAIEMENT                                            │
│    - Sélection méthode(s)                               │
│    - Validation montant                                 │
│    - Calcul monnaie                                     │
│    - Impression ticket                                  │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│ 6. ACCUMULATION POINTS                                 │
│    - Calcul points gagnés                               │
│    - Mise à jour solde client                           │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│ 7. FIN DE JOURNÉE                                      │
│    - Clôture automatique                                │
│    - Génération rapport Z                               │
│    - Archivage                                          │
└─────────────────────────────────────────────────────────┘
```

---

## Intégration avec le backend

### Configuration

Fichier `.env` à la racine :
```env
VUE_APP_API_URL=http://localhost:8000/api
```

### Headers HTTP

Tous les appels API incluent automatiquement :
```javascript
{
  'Content-Type': 'application/json',
  'Accept': 'application/json',
  'Authorization': 'Bearer <token>' // Si disponible
}
```

### Gestion des erreurs

Les erreurs sont gérées globalement via les intercepteurs Axios :

```javascript
// Intercepteur de réponse
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Déconnexion automatique
      localStorage.removeItem('auth_token');
    }
    return Promise.reject(error);
  }
);
```

### Format des données

#### Transaction
```json
{
  "id": "uuid",
  "transaction_number": "TXN-20250124-001",
  "date": "2025-01-24T10:30:00Z",
  "cashier_id": "CAISSE-001",
  "items": [
    {
      "product_id": "PROD-001",
      "product_name": "Savon",
      "quantity": 2,
      "unit_price": 500,
      "total_price": 1000,
      "discount": 50
    }
  ],
  "subtotal": 950,
  "total_discount": 50,
  "tax_amount": 171,
  "total_amount": 1121,
  "payments": [
    {
      "method": "cash",
      "amount": 2000,
      "change_due": 879
    }
  ],
  "status": "completed"
}
```

---

## Bonnes pratiques

### 1. Gestion des erreurs
```javascript
try {
  const data = await transactionsAPI.getAllTransactions();
} catch (error) {
  console.error('Erreur:', error);
  // Afficher notification utilisateur
  this.showNotification('error', 'Impossible de charger les transactions');
}
```

### 2. Loading states
```javascript
async loadData() {
  this.loading = true;
  try {
    this.data = await API.getData();
  } finally {
    this.loading = false; // Toujours exécuté
  }
}
```

### 3. Formatage des montants
```javascript
formatPrice(amount) {
  return new Intl.NumberFormat('fr-FR', {
    style: 'currency',
    currency: 'XOF',
    minimumFractionDigits: 0
  }).format(amount);
}
```

### 4. Validation des inputs
```javascript
// Toujours valider avant envoi API
if (!this.cart.length) {
  alert('Le panier est vide');
  return;
}

if (this.total <= 0) {
  alert('Montant invalide');
  return;
}
```

---

## Support et maintenance

Pour toute question ou problème :
- 📧 Email : support@expressmall.com
- 📖 Documentation complète : `/docs`
- 🐛 Rapporter un bug : GitHub Issues

---

**Dernière mise à jour** : 24 janvier 2025
