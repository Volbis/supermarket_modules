<template>
  <div class="orders-page">
    <!-- Cartes de statistiques -->
        <!-- Stats Cards -->
    <div class="stats-container">
      <div class="stat-card">
        <div class="stat-icon" style="background: #e3f2fd">
          <i class="fas fa-shopping-cart" style="color: #1976d2"></i>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ stats.totalMois }}</div>
          <div class="stat-label">Commandes ce mois</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon" style="background: #fff3cd">
          <i class="fas fa-clock" style="color: #ff9800"></i>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ stats.enCours }}</div>
          <div class="stat-label">Commandes en cours</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon" style="background: #d4edda">
          <i class="fas fa-truck" style="color: #4caf50"></i>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ stats.totalFournisseurs }}</div>
          <div class="stat-label">Fournisseurs actifs</div>
        </div>
      </div>
    </div>

    <!-- Barre de recherche -->

    <div class="search-bar-container">
        <div class="search-wrapper">
            <span class="search-icon">🔍</span>
            <div class="input-bg">
                <input type="text" placeholder="Rechercher commande" v-model="searchQuery">
            </div>
            <div class="status-bg">
                <select v-model="selectedStatus" class="status-filter">
                    <option value="">Tous les statuts</option>
                    <option value="EN_COURS">En cours</option>
                    <option value="LIVREE">Livrée</option>
                    <option value="ANNULEE">Annulée</option>
                </select>
            </div>
        </div>
        <button class="pass-order-btn" @click="openModal">
            <span class="btn-icon">
              <img src="@/assets/icons/plus.png" alt="Nouvelle commande" style="width: 1em; color: white; height: 1em; vertical-align: middle; margin-right: 5px;">
            </span>
            Passer commande
        </button>
    </div>


    <!-- Tableau des commandes -->
    <div class="orders-list-container">
      <h2>Liste des commandes</h2>
      
      <table class="orders-table">
        <thead>
          <tr>
            <th>Produit</th>
            <th>Qte</th>
            <th>Fournisseur</th>
            <th>Date Arrivage</th>
            <th>Statut</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="loading">
            <td colspan="6" style="text-align: center; padding: 40px;">
              Chargement des commandes...
            </td>
          </tr>
          <tr v-else-if="filteredCommandes.length === 0">
            <td colspan="6" style="text-align: center; padding: 40px;">
              Aucune commande trouvée
            </td>
          </tr>
          <tr v-else v-for="commande in filteredCommandes" :key="commande.id_commande">
            <td>{{ getCommandeProducts(commande.id_commande) }}</td>
            <td>{{ getCommandeQuantite(commande.id_commande) }}</td>
            <td>{{ getFournisseurName(commande.fournisseur) }}</td>
            <td>{{ formatDate(commande.date_livraison_prevue) }}</td>
            <td>
              <span :class="['status-badge', mapDjangoStatusToFrontend(commande.statut)]">
                {{ getStatusLabel(commande.statut) }}
              </span>
            </td>
            <td class="actions-cell">
              <button 
                v-if="commande.statut === 'EN_COURS'" 
                class="action-icon" 
                title="Valider"
                @click="validerCommande(commande)">
                ✅
              </button>
              <button 
                v-if="commande.statut === 'EN_COURS'" 
                class="action-icon delete" 
                title="Annuler"
                @click="annulerCommande(commande)">
                ❌
              </button>
              <button 
                class="action-icon" 
                title="Détails"
                @click="voirDetailsCommande(commande)">
                👁️
              </button>
              <button 
                class="action-icon delete" 
                title="Supprimer"
                @click="deleteCommande(commande)">
                🗑️
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>

  <!-- Modal: Nouvelle commande -->
  <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
    <div class="modal-card">
      <div class="modal-header">
        <h3>Nouvelle commande</h3>
        <button class="close-btn" @click="closeModal">✕</button>
      </div>
      <form class="modal-body" @submit.prevent="submitOrder">
        <div class="form-row">
          <label for="supplier">Fournisseur</label>
          <select id="supplier" v-model="form.fournisseur" required>
            <option value="">-- Sélectionner un fournisseur --</option>
            <option 
              v-for="fournisseur in fournisseurs" 
              :key="fournisseur.id_fournisseur" 
              :value="fournisseur.id_fournisseur">
              {{ fournisseur.nom }}
            </option>
          </select>
        </div>

        <div class="form-row">
          <label for="arrivalDate">Date de livraison prévue</label>
          <input id="arrivalDate" v-model="form.date_livraison_prevue" type="date" required>
        </div>

        <div class="form-row">
          <label for="status">Statut</label>
          <select id="status" v-model="form.statut" required>
            <option value="EN_COURS">En cours</option>
            <option value="LIVREE">Livrée</option>
            <option value="ANNULEE">Annulée</option>
          </select>
        </div>

        <!-- Section Produits -->
        <div style="margin-top: 20px; border-top: 1px solid #eee; padding-top: 20px;">
          <h4 style="margin-bottom: 15px;">Produits de la commande</h4>
          
          <div 
            v-for="(produitItem, index) in form.produits" 
            :key="index"
            style="display: flex; gap: 10px; margin-bottom: 10px; align-items: flex-end;">
            
            <div class="form-row" style="flex: 2; margin: 0;">
              <label :for="'produit-' + index">Produit</label>
              <select 
                :id="'produit-' + index" 
                v-model="produitItem.produit" 
                required>
                <option value="">-- Sélectionner un produit --</option>
                <option 
                  v-for="produit in produits" 
                  :key="produit.id_product" 
                  :value="produit.id_product">
                  {{ produit.nom }}
                </option>
              </select>
            </div>

            <div class="form-row" style="flex: 1; margin: 0;">
              <label :for="'quantite-' + index">Quantité</label>
              <input 
                :id="'quantite-' + index" 
                v-model="produitItem.quantite" 
                type="number" 
                min="1"
                placeholder="Ex: 100" 
                required>
            </div>

            <button 
              v-if="form.produits.length > 1"
              type="button"
              @click="supprimerProduit(index)"
              class="btn-secondary"
              style="height: 40px; padding: 0 15px;">
              ✕
            </button>
          </div>

          <button 
            type="button"
            @click="ajouterProduit"
            class="btn-secondary"
            style="margin-top: 10px;">
            + Ajouter un produit
          </button>
        </div>

        <div class="modal-actions">
          <button type="button" class="btn-secondary" @click="closeModal">Annuler</button>
          <button type="submit" class="btn-primary" :disabled="loading">
            {{ loading ? 'Création...' : 'Créer la commande' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { commandesAPI, produitsAPI, fournisseursAPI, detailsCommandesAPI } from '@/services';
import { useDataCache } from '@/composables/useDataCache';

export default {
  name: 'OrdersManagementPage',
  setup() {
    const { loadWithCache, invalidateCache, isCacheValid } = useDataCache();
    return { loadWithCache, invalidateCache, isCacheValid };
  },
  data() {
    return {
      searchQuery: '',
      selectedStatus: '',
      showModal: false,
      loading: true, // Commencer en loading pour éviter le flash "Aucune commande"
      error: null,
      
      // Données du backend
      commandes: [],
      produits: [],
      fournisseurs: [],
      details: [],
      
      // Statistiques
      stats: {
        totalMois: 0,
        enCours: 0,
        totalFournisseurs: 0
      },
      
      form: {
        fournisseur: '',
        date_livraison_prevue: '',
        statut: 'EN_COURS',
        produits: [
          {
            produit: '',
            quantite: ''
          }
        ]
      }
    };
  },
  mounted() {
    // Charger avec cache si disponible
    this.loadData(false);
  },
  computed: {
    filteredCommandes() {
      return this.commandes.filter(commande => {
        const matchesSearch =
          this.getCommandeProducts(commande.id_commande).toLowerCase().includes(this.searchQuery.toLowerCase()) ||
          this.getFournisseurName(commande.fournisseur).toLowerCase().includes(this.searchQuery.toLowerCase());
        const matchesStatus = !this.selectedStatus || commande.statut === this.selectedStatus;
        return matchesSearch && matchesStatus;
      });
    }
  },
  methods: {
    // === MÉTHODE PUBLIQUE POUR REFRESH DEPUIS APP.VUE ===
    async refreshData() {
      console.log('🔄 Rafraîchissement forcé des Commandes...');
      this.invalidateCache('commandes');
      this.invalidateCache('produits');
      this.invalidateCache('fournisseurs');
      await this.loadData(true);
      alert('✅ Commandes actualisées');
    },
    
    /**
     * Charge toutes les données depuis l'API
     */
    async loadData(forceRefresh = false) {
      // Ne montrer le loading QUE si:
      // - On force le refresh OU
      // - Le cache n'est pas valide (expiré ou inexistant)
      const cacheDisponible = this.isCacheValid('commandes') && 
                              this.isCacheValid('produits') && 
                              this.isCacheValid('fournisseurs');
      const showLoading = forceRefresh || !cacheDisponible;
      
      if (showLoading) {
        this.loading = true;
      }
      this.error = null;
      
      try {
        // Charger toutes les données en parallèle avec cache
        const [commandesData, produitsData, fournisseursData, detailsData] = await Promise.all([
          this.loadWithCache('commandes', async () => {
            const res = await commandesAPI.getAllCommandes();
            console.log('📦 Commandes chargées depuis l\'API:', res.data.length);
            return res.data;
          }, forceRefresh),
          this.loadWithCache('produits', async () => {
            const res = await produitsAPI.getAllProduits();
            console.log('📦 Produits chargés depuis l\'API:', res.data.length);
            return res.data;
          }, forceRefresh),
          this.loadWithCache('fournisseurs', async () => {
            const res = await fournisseursAPI.getAllFournisseurs();
            console.log('📦 Fournisseurs chargés depuis l\'API:', res.data.length);
            return res.data;
          }, forceRefresh),
          detailsCommandesAPI.getAllDetailsCommandes().then(res => res.data)
        ]);
        
        this.commandes = commandesData;
        this.produits = produitsData;
        this.fournisseurs = fournisseursData;
        this.details = detailsData;
        
        // Calculer les statistiques
        this.calculateStats();
        
        console.log('Données chargées:', {
          commandes: this.commandes.length,
          produits: this.produits.length,
          fournisseurs: this.fournisseurs.length,
          details: this.details.length
        });
        
      } catch (err) {
        this.error = 'Erreur lors du chargement des données';
        console.error('Erreur:', err);
        alert('Erreur lors du chargement des commandes');
      } finally {
        // Toujours désactiver le loading, même si on a utilisé le cache
        this.loading = false;
      }
    },
    
    /**
     * Calcule les statistiques pour les cartes
     */
    calculateStats() {
      const now = new Date();
      const currentMonth = now.getMonth();
      const currentYear = now.getFullYear();
      
      // Total des commandes du mois en cours
      this.stats.totalMois = this.commandes.filter(cmd => {
        const cmdDate = new Date(cmd.date_commande);
        return cmdDate.getMonth() === currentMonth && cmdDate.getFullYear() === currentYear;
      }).length;
      
      // Commandes en cours
      this.stats.enCours = this.commandes.filter(cmd => cmd.statut === 'EN_COURS').length;
      
      // Total fournisseurs
      this.stats.totalFournisseurs = this.fournisseurs.length;
    },
    
    /**
     * Récupère les produits d'une commande
     */
    getCommandeProducts(commandeId) {
      const commandeDetails = this.details.filter(d => d.commande === commandeId);
      return commandeDetails.map(d => {
        const produit = this.produits.find(p => p.id_product === d.produit);
        return produit ? `${produit.nom} (${d.quantite})` : 'Produit inconnu';
      }).join(', ') || 'Aucun produit';
    },
    
    /**
     * Récupère la quantité totale d'une commande
     */
    getCommandeQuantite(commandeId) {
      const commandeDetails = this.details.filter(d => d.commande === commandeId);
      const total = commandeDetails.reduce((sum, d) => sum + d.quantite, 0);
      return `${total} unités`;
    },
    
    /**
     * Récupère le nom du fournisseur
     */
    getFournisseurName(fournisseurId) {
      const fournisseur = this.fournisseurs.find(f => f.id_fournisseur === fournisseurId);
      return fournisseur ? fournisseur.nom : 'Fournisseur inconnu';
    },
    
    /**
     * Formate une date
     */
    formatDate(dateString) {
      if (!dateString) return '';
      const date = new Date(dateString);
      const day = String(date.getDate()).padStart(2, '0');
      const month = String(date.getMonth() + 1).padStart(2, '0');
      const year = date.getFullYear();
      return `${day}/${month}/${year}`;
    },
    
    /**
     * Mapper les statuts Django vers les statuts frontend
     */
    mapDjangoStatusToFrontend(djangoStatus) {
      const mapping = {
        'EN_COURS': 'processing',
        'LIVREE': 'delivered',
        'ANNULEE': 'cancelled'
      };
      return mapping[djangoStatus] || 'pending';
    },
    
    /**
     * Mapper les statuts frontend vers Django
     */
    mapFrontendStatusToDjango(frontendStatus) {
      const mapping = {
        'processing': 'EN_COURS',
        'delivered': 'LIVREE',
        'cancelled': 'ANNULEE',
        'pending': 'EN_COURS'
      };
      return mapping[frontendStatus] || 'EN_COURS';
    },
    
    getStatusLabel(status) {
      const labels = {
        'EN_COURS': 'En Cours',
        'LIVREE': 'Livrée',
        'ANNULEE': 'Annulée',
        'processing': 'En Cours',
        'delivered': 'Livrée',
        'cancelled': 'Annulée',
        'pending': 'En Attente'
      };
      return labels[status] || status;
    },
    
    /**
     * Ouvre le modal pour créer une nouvelle commande
     */
    openModal() {
      this.resetForm();
      this.showModal = true;
    },
    
    /**
     * Ferme le modal
     */
    closeModal() {
      this.showModal = false;
    },
    
    /**
     * Soumet une nouvelle commande
     */
    async submitOrder() {
      if (!this.form.fournisseur || !this.form.date_livraison_prevue) {
        alert('Veuillez remplir tous les champs obligatoires');
        return;
      }
      
      // Vérifier qu'il y a au moins un produit
      const produitsValides = this.form.produits.filter(p => p.produit && p.quantite > 0);
      if (produitsValides.length === 0) {
        alert('Veuillez ajouter au moins un produit à la commande');
        return;
      }
      
      this.loading = true;
      
      try {
        // 1. Créer la commande d'approvisionnement
        const commandeData = {
          fournisseur: this.form.fournisseur,
          date_livraison_prevue: new Date(this.form.date_livraison_prevue).toISOString(),
          statut: this.form.statut
        };
        
        const commandeRes = await commandesAPI.createCommande(commandeData);
        const nouvelleCommande = commandeRes.data;
        
        console.log('Commande créée:', nouvelleCommande);
        
        // 2. Créer les détails de commande pour chaque produit
        for (const produitItem of produitsValides) {
          const detailData = {
            commande: nouvelleCommande.id_commande,
            produit: produitItem.produit,
            quantite: parseInt(produitItem.quantite)
          };
          
          await detailsCommandesAPI.createDetailCommande(detailData);
        }
        
        console.log('Détails de commande créés');
        
        // 3. Invalider le cache et recharger les données
        this.invalidateCache('commandes');
        await this.loadData(true);
        
        // 4. Fermer le modal
        this.closeModal();
        
        alert('Commande créée avec succès !');
        
      } catch (err) {
        console.error('Erreur lors de la création de la commande:', err);
        alert(err.response?.data?.message || 'Erreur lors de la création de la commande');
      } finally {
        this.loading = false;
      }
    },
    
    /**
     * Ajoute une ligne de produit au formulaire
     */
    ajouterProduit() {
      this.form.produits.push({
        produit: '',
        quantite: ''
      });
    },
    
    /**
     * Supprime une ligne de produit du formulaire
     */
    supprimerProduit(index) {
      if (this.form.produits.length > 1) {
        this.form.produits.splice(index, 1);
      }
    },
    
    /**
     * Réinitialise le formulaire
     */
    resetForm() {
      this.form = {
        fournisseur: '',
        date_livraison_prevue: '',
        statut: 'EN_COURS',
        produits: [
          {
            produit: '',
            quantite: ''
          }
        ]
      };
    },
    
    /**
     * Valide une commande
     */
    async validerCommande(commande) {
      if (!confirm(`Valider la commande pour ${this.getFournisseurName(commande.fournisseur)} ?`)) {
        return;
      }
      
      try {
        await commandesAPI.validerCommande(commande.id_commande);
        await this.loadData();
        alert('Commande validée avec succès !');
      } catch (err) {
        console.error('Erreur:', err);
        alert('Erreur lors de la validation de la commande');
      }
    },
    
    /**
     * Annule une commande
     */
    async annulerCommande(commande) {
      if (!confirm(`Annuler la commande pour ${this.getFournisseurName(commande.fournisseur)} ?`)) {
        return;
      }
      
      try {
        await commandesAPI.annulerCommande(commande.id_commande);
        await this.loadData();
        alert('Commande annulée avec succès !');
      } catch (err) {
        console.error('Erreur:', err);
        alert('Erreur lors de l\'annulation de la commande');
      }
    },
    
    /**
     * Supprime une commande
     */
    async deleteCommande(commande) {
      if (!confirm(`Supprimer définitivement la commande pour ${this.getFournisseurName(commande.fournisseur)} ?`)) {
        return;
      }
      
      try {
        await commandesAPI.deleteCommande(commande.id_commande);
        
        // Invalider le cache et recharger
        this.invalidateCache('commandes');
        await this.loadData(true);
        
        alert('Commande supprimée avec succès !');
      } catch (err) {
        console.error('Erreur:', err);
        alert('Erreur lors de la suppression de la commande');
      }
    },
    
    /**
     * Affiche les détails d'une commande
     */
    voirDetailsCommande(commande) {
      const details = this.details.filter(d => d.commande === commande.id_commande);
      const produitsInfo = details.map(d => {
        const produit = this.produits.find(p => p.id_product === d.produit);
        return `- ${produit?.nom || 'Inconnu'}: ${d.quantite} unités`;
      }).join('\n');
      
      alert(`Détails de la commande:\n\nFournisseur: ${this.getFournisseurName(commande.fournisseur)}\nDate: ${this.formatDate(commande.date_commande)}\nLivraison prévue: ${this.formatDate(commande.date_livraison_prevue)}\nStatut: ${this.getStatusLabel(commande.statut)}\n\nProduits:\n${produitsInfo}`);
    }
  }
};
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.orders-page {
  padding: 20px;
  background: #F9F9FA;
  min-height: 100vh;
}

/* Cartes de statistiques */
.stats-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.stat-card {
  background: white;
  border-radius: 17px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  border: 1px solid #e0e0e0;
}

.stat-content {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 15px;
}

.stat-card h3 {
  font-size: 14px;
  font-weight: 500;
  color: #666;
  flex: 1;
}

.stat-icon {
  font-size: 32px;
  margin-left: 10px;
}

.stat-bar {
  height: 3px;
  width: 10%;
  border-radius: 2px;
  margin-left: 0;
}

/* Couleurs différentes pour chaque card */
.stats-container .stat-card:nth-child(1) .stat-bar {
  background: linear-gradient(to right, #ffc107, #ffecb3); /* Jaune doré */
}
.stats-container .stat-card:nth-child(2) .stat-bar {
  background: linear-gradient(to right, #2196f3, #b3e5fc); /* Bleu */
}
.stats-container .stat-card:nth-child(3) .stat-bar {
  background: linear-gradient(to right, #4caf50, #c8e6c9); /* Vert */
}


/* Barre de recherche */
.search-bar-container {

  width: 100%;
  height: 45px;
  display: flex;
  gap: 10px;
  margin-bottom: 30px;
  border-radius: 17px;
  align-items: center;
}

.search-wrapper {
  flex: 1;
  display: flex;
  align-items: center;
  background: white;
  border-radius: 17px;
  padding: 0 20px;
  gap: 12px;
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.15);
}

.search-icon {
  font-size: 18px;
  color: #999;
  flex-shrink: 0;
}

.search-wrapper input {
  flex: 1;
  border: none;
  outline: none;
  padding: 12px 0;
  font-size: 14px;
  background: transparent;
  color: #333;
}

.search-wrapper input::placeholder {
  color: #999;
}

.status-filter {
  padding: 8px 12px;
  border: none;
  background: transparent;
  cursor: pointer;
  font-size: 14px;
  color: #666;
  outline: none;
  flex-shrink: 0;
}

.status-filter option {
  color: #333;
}

.pass-order-btn {
  background: #D08700;
  color: white;
  border: none;
  padding: 12px 28px;
  border-radius: 25px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  box-shadow: 0 4px 12px rgba(255, 193, 7, 0.35);
  transition: all 0.3s ease;
  white-space: nowrap;
  font-size: 14px;
}


.pass-order-btn:active {
  transform: translateY(0);
}

.btn-icon {
  font-size: 16px;
  display: flex;
  align-items: center;
}

@media (max-width: 768px) {
  .search-bar-container {
    flex-direction: column;
    gap: 12px;
  }

  .search-wrapper {
    width: 100%;
  }

  .pass-order-btn {
    width: 100%;
    justify-content: center;
  }
}

/* barre backgrounds */
.input-bg {
  background:rgba(249, 249, 249, 0);
  border-radius: 17px;
  padding: 0 10px;
  width: 80%;
  height: 80%;
}

.status-bg {
  background: #f9f9f9;
  border-radius: 17px;
  padding: 0 10px;
  height: 100%;
  border: 1px solid #F5F5F5;
}

/* Tableau des commandes */
.orders-list-container {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.orders-list-container h2 {
  font-size: 18px;
  font-weight: 600;
  color: #333;
  margin-bottom: 20px;
}

.orders-table {
  width: 100%;
  border-collapse: collapse;
}

.orders-table th {
  background: #f9f9f9;
  padding: 15px;
  text-align: left;
  font-weight: 600;
  font-size: 14px;
  color: #666;
  border-bottom: 2px solid #e0e0e0;
}

.orders-table td {
  padding: 15px;
  border-bottom: 1px solid #e0e0e0;
  font-size: 14px;
  color: #333;
}

.orders-table tbody tr:hover {
  background: #fafafa;
}

.status-badge {
  display: inline-block;
  min-width: 110px;
  text-align: center;
  box-sizing: border-box;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  text-transform: capitalize;
}

.status-badge.pending {
  background: #fff3cd;
  color: #856404;
}

.status-badge.processing {
  background: #cce5ff;
  color: #003d99;
}

.status-badge.shipped {
  background: #d4edda;
  color: #155724;
}

.status-badge.delivered {
  background: #e2d9f3;
  color: #6f42c1;
}

.actions-cell {
  display: flex;
  gap: 10px;
}

.action-icon {
  background: none;
  border: none;
  font-size: 16px;
  cursor: pointer;
  transition: transform 0.2s;
  padding: 4px 8px;
}

.action-icon:hover {
  transform: scale(1.2);
}

.action-icon.delete:hover {
  color: red;
}

/* Responsive */
@media (max-width: 768px) {
  .stats-container {
    grid-template-columns: 1fr;
  }

  .search-bar-container {
    flex-direction: column;
  }

  .search-wrapper {
    width: 100%;
  }

  .pass-order-btn {
    width: 100%;
    justify-content: center;
  }

  .orders-table th,
  .orders-table td {
    padding: 10px;
    font-size: 12px;
  }
}

/* Modal styles */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.45);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  z-index: 1000;
}

.modal-card {
  width: 100%;
  max-width: 520px;
  background: #ffffff;
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.12);
  overflow: hidden;
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  border-bottom: 1px solid #f0f0f0;
}

.modal-header h3 {
  font-size: 16px;
  font-weight: 600;
  color: #333;
}

.close-btn {
  background: transparent;
  border: none;
  font-size: 18px;
  cursor: pointer;
  padding: 6px 8px;
}

.modal-body {
  padding: 18px 20px 20px 20px;
}

.form-row {
  display: flex;
  flex-direction: column;
  gap: 6px;
  margin-bottom: 14px;
}

.form-row label {
  font-size: 13px;
  color: #555;
}

.form-row input,
.form-row select {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  background: #fff;
  font-size: 14px;
  outline: none;
}

.form-row input:focus,
.form-row select:focus {
  border-color: #93c5fd;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15);
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 8px;
}

.btn-secondary {
  background: #f3f4f6;
  color: #374151;
  border: 1px solid #e5e7eb;
  padding: 10px 16px;
  border-radius: 10px;
  font-weight: 600;
  cursor: pointer;
}

.btn-primary {
  background: #2563eb;
  color: #ffffff;
  border: none;
  padding: 10px 16px;
  border-radius: 10px;
  font-weight: 600;
  cursor: pointer;
  box-shadow: 0 8px 18px rgba(37, 99, 235, 0.25);
}
</style>