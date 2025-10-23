# 📚 Services API - Documentation

Ce dossier contient tous les services API pour communiquer avec le backend Django de l'application supermarket.

## 📁 Structure des Services

```
services/
├── index.js                # Point d'entrée centralisé
├── categories.js           # Gestion des catégories de produits
├── produits.js             # Gestion des produits
├── fournisseurs.js         # Gestion des fournisseurs
├── stocks.js               # Gestion des stocks
├── commandes.js            # Gestion des commandes d'approvisionnement
├── detailsCommandes.js     # Gestion des détails de commandes
├── alertes.js              # Gestion des alertes de stock
├── historiqueStock.js      # Historique des mouvements de stock
├── responsables.js         # Gestion des responsables de stock
└── historiqueVentes.js     # Historique et statistiques des ventes
```

## 🚀 Utilisation

### Import Simple (recommandé)

```javascript
// Import d'un service spécifique
import { categoriesAPI, produitsAPI } from '@/services';

// Utilisation
const categories = await categoriesAPI.getAllCategories();
const produits = await produitsAPI.getAllProduits();
```

### Import Global

```javascript
// Import de tous les services
import services from '@/services';

// Utilisation
const categories = await services.categoriesAPI.getAllCategories();
```

### Import Direct

```javascript
// Import direct depuis le fichier du service
import categoriesAPI from '@/services/categories';

const categories = await categoriesAPI.getAllCategories();
```

## 📋 Services Disponibles

### 1. **categoriesAPI** - Gestion des Catégories

```javascript
import { categoriesAPI } from '@/services';

// Récupérer toutes les catégories
const categories = await categoriesAPI.getAllCategories();

// Récupérer une catégorie par ID
const categorie = await categoriesAPI.getCategoryById(id);

// Créer une catégorie
const newCategory = await categoriesAPI.createCategory({
  nom: 'BOISSON',
  description: 'Boissons et breuvages'
});

// Mettre à jour une catégorie
await categoriesAPI.updateCategory(id, { nom: 'BOISSON', description: '...' });

// Mise à jour partielle
await categoriesAPI.patchCategory(id, { description: 'Nouvelle description' });

// Supprimer une catégorie
await categoriesAPI.deleteCategory(id);

// Récupérer les produits d'une catégorie
const produits = await categoriesAPI.getCategoryProducts(id);
```

### 2. **produitsAPI** - Gestion des Produits

```javascript
import { produitsAPI } from '@/services';

// Récupérer tous les produits
const produits = await produitsAPI.getAllProduits();

// Récupérer un produit par ID
const produit = await produitsAPI.getProduitById(id);

// Créer un produit
const newProduit = await produitsAPI.createProduit({
  nom: 'Coca Cola',
  reference: 'REF001',
  designation: 'Boisson gazeuse 33cl',
  prix_unitaire: 1.50,
  quantite_en_stock: 100,
  seuil_de_reapprovisionnement: 20,
  date_de_peremption: '2025-12-31',
  categorie: 'uuid-categorie',
  fournisseur: 'uuid-fournisseur'
});

// Mettre à jour un produit
await produitsAPI.updateProduit(id, produitData);

// Mise à jour partielle
await produitsAPI.patchProduit(id, { quantite_en_stock: 150 });

// Supprimer un produit
await produitsAPI.deleteProduit(id);

// Récupérer les produits sous seuil
const sousSeuilProduits = await produitsAPI.getProduitsSousSeuil();

// Récupérer les produits périmés
const produitPerimes = await produitsAPI.getProduitsPerimes();
```

### 3. **fournisseursAPI** - Gestion des Fournisseurs

```javascript
import { fournisseursAPI } from '@/services';

// Récupérer tous les fournisseurs
const fournisseurs = await fournisseursAPI.getAllFournisseurs();

// Créer un fournisseur
const newFournisseur = await fournisseursAPI.createFournisseur({
  nom: 'Coca Cola Company',
  contact: '+225 01 02 03 04 05',
  adresse: 'Abidjan, Cocody',
  catalogue_produits: 'Boissons gazeuses, jus',
  delais_livraison_jours: 7
});

// Récupérer les produits d'un fournisseur
const produits = await fournisseursAPI.getFournisseurProduits(id);
```

### 4. **stocksAPI** - Gestion des Stocks

```javascript
import { stocksAPI } from '@/services';

// Récupérer tous les stocks
const stocks = await stocksAPI.getAllStocks();

// Créer un stock
const newStock = await stocksAPI.createStock({
  produit: 'uuid-produit',
  quantite: 100
});

// Ajouter du stock
await stocksAPI.ajouterStock(id, 50);

// Retirer du stock
await stocksAPI.retirerStock(id, 20);
```

### 5. **commandesAPI** - Gestion des Commandes

```javascript
import { commandesAPI } from '@/services';

// Récupérer toutes les commandes
const commandes = await commandesAPI.getAllCommandes();

// Créer une commande
const newCommande = await commandesAPI.createCommande({
  fournisseur: 'uuid-fournisseur',
  date_livraison_prevue: '2025-11-01T10:00:00Z',
  statut: 'EN_COURS'
});

// Valider une commande
await commandesAPI.validerCommande(id);

// Annuler une commande
await commandesAPI.annulerCommande(id);

// Obtenir le montant total
const montant = await commandesAPI.getMontantTotal(id);
```

### 6. **detailsCommandesAPI** - Détails des Commandes

```javascript
import { detailsCommandesAPI } from '@/services';

// Créer un détail de commande
const detail = await detailsCommandesAPI.createDetailCommande({
  commande: 'uuid-commande',
  produit: 'uuid-produit',
  quantite: 50
});

// Obtenir le sous-total
const sousTotal = await detailsCommandesAPI.getSousTotal(id);
```

### 7. **alertesAPI** - Gestion des Alertes

```javascript
import { alertesAPI } from '@/services';

// Récupérer toutes les alertes
const alertes = await alertesAPI.getAllAlertes();

// Créer une alerte
const newAlerte = await alertesAPI.createAlerte({
  produit: 'uuid-produit',
  message: 'Stock faible - Réapprovisionnement nécessaire'
});

// Récupérer les alertes actives
const alertesActives = await alertesAPI.getAlertesActives();

// Récupérer les alertes d'un produit
const alertesProduit = await alertesAPI.getAlertesByProduit(produitId);
```

### 8. **historiqueStockAPI** - Historique des Stocks

```javascript
import { historiqueStockAPI } from '@/services';

// Récupérer tout l'historique
const historique = await historiqueStockAPI.getAllHistoriqueStock();

// Créer un enregistrement d'historique
const newHistorique = await historiqueStockAPI.createHistoriqueStock({
  produit: 'uuid-produit',
  quantite_modifiee: 50,
  type_modification: 'AJOUT'
});

// Historique par produit
const histProduit = await historiqueStockAPI.getHistoriqueByProduit(produitId);

// Historique par type
const histAjouts = await historiqueStockAPI.getHistoriqueByType('AJOUT');

// Historique par période
const histPeriode = await historiqueStockAPI.getHistoriqueByPeriode(
  '2025-01-01',
  '2025-12-31'
);
```

### 9. **responsablesAPI** - Gestion des Responsables

```javascript
import { responsablesAPI } from '@/services';

// Récupérer tous les responsables
const responsables = await responsablesAPI.getAllResponsables();

// Créer un responsable
const newResponsable = await responsablesAPI.createResponsable({
  nom: 'Jean Dupont',
  email: 'jean.dupont@supermarket.com',
  telephone: '+225 01 02 03 04 05'
});

// Valider une commande via un responsable
await responsablesAPI.validerCommande(responsableId, commandeId);

// Consulter le rapport d'inventaire
const rapport = await responsablesAPI.consulterRapportInventaire(responsableId);
```

### 10. **historiqueVentesAPI** - Historique des Ventes

```javascript
import { historiqueVentesAPI } from '@/services';

// Récupérer tout l'historique des ventes
const ventes = await historiqueVentesAPI.getAllHistoriqueVentes();

// Créer un enregistrement de vente
const newVente = await historiqueVentesAPI.createHistoriqueVente({
  produit: 'uuid-produit',
  quantite_vendue: 10,
  montant_total: 15.00,
  chiffre_affaires_journalier: 1500.00
});

// Ventes par produit
const ventesProduit = await historiqueVentesAPI.getVentesByProduit(produitId);

// Ventes par période
const ventesPeriode = await historiqueVentesAPI.getVentesByPeriode(
  '2025-01-01',
  '2025-12-31'
);

// Obtenir la tendance des ventes
const tendance = await historiqueVentesAPI.getTendanceVente(id);

// Prévision de demande
const prevision = await historiqueVentesAPI.getProvisionDemande(id);

// Chiffre d'affaires total
const ca = await historiqueVentesAPI.getChiffAffairesTotal('2025-01-01', '2025-12-31');
```

## 🔧 Gestion des Erreurs

Tous les services retournent des Promises. Utilisez try-catch pour gérer les erreurs :

```javascript
try {
  const categories = await categoriesAPI.getAllCategories();
  console.log('Catégories:', categories.data);
} catch (error) {
  console.error('Erreur:', error.response?.data?.message || error.message);
  // Afficher un message à l'utilisateur
}
```

## 📝 Structure des Réponses

Toutes les réponses API suivent cette structure :

```javascript
{
  data: { ... },      // Données de la réponse
  status: 200,        // Code HTTP
  statusText: 'OK',   // Message du statut
  headers: { ... },   // En-têtes de la réponse
  config: { ... }     // Configuration de la requête
}
```

Accédez aux données avec `response.data` :

```javascript
const response = await categoriesAPI.getAllCategories();
const categories = response.data; // Tableau des catégories
```

## 🎯 Bonnes Pratiques

1. **Toujours utiliser try-catch** pour gérer les erreurs
2. **Importer uniquement les services nécessaires** pour optimiser le bundle
3. **Utiliser async/await** plutôt que .then()/.catch()
4. **Vérifier les données** avant de les envoyer au backend
5. **Afficher des messages utilisateur** en cas d'erreur

## 🔗 Configuration de Base

La configuration axios de base se trouve dans `/src/api/api.js` :

```javascript
import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000/api/stocks/",
});

export default api;
```

Pour modifier l'URL de base ou ajouter des intercepteurs, modifiez ce fichier.

## 📞 Support

Pour toute question ou problème, consultez la documentation Django du backend ou contactez l'équipe de développement.
