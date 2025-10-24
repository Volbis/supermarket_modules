<template>
  <div class="closing-content">
    <div class="page-header">
      <div>
        <h2>🔒 Clôture de Caisse</h2>
        <p class="subtitle">Fermez la caisse et générez le rapport de fin de journée</p>
      </div>
      <div class="closing-status">
        <span class="status-indicator" :class="closingStatus"></span>
        <span class="status-text">{{ getStatusText() }}</span>
      </div>
    </div>

    <!-- Étape actuelle -->
    <div class="steps-indicator">
      <div 
        v-for="(step, index) in steps" 
        :key="index"
        :class="['step', { active: currentStep === index, completed: currentStep > index }]"
      >
        <div class="step-number">{{ index + 1 }}</div>
        <div class="step-label">{{ step }}</div>
      </div>
    </div>

    <!-- Étape 1: Comptage du fond de caisse -->
    <div v-if="currentStep === 0" class="section-card">
      <h3>💵 Comptage du Fond de Caisse</h3>
      <p class="section-description">Comptez les billets et pièces présents dans la caisse</p>

      <div class="cash-counting">
        <!-- Billets -->
        <div class="denomination-group">
          <h4>Billets</h4>
          <div class="denominations-grid">
            <div 
              v-for="bill in bills" 
              :key="bill.value"
              class="denomination-item"
            >
              <div class="denomination-header">
                <span class="denomination-value">{{ formatPrice(bill.value) }}</span>
                <span class="denomination-icon">💵</span>
              </div>
              <input 
                type="number" 
                v-model.number="bill.count" 
                @input="calculateTotal"
                min="0"
                class="count-input"
                placeholder="0"
              />
              <div class="denomination-total">
                {{ formatPrice(bill.value * bill.count) }}
              </div>
            </div>
          </div>
        </div>

        <!-- Pièces -->
        <div class="denomination-group">
          <h4>Pièces</h4>
          <div class="denominations-grid">
            <div 
              v-for="coin in coins" 
              :key="coin.value"
              class="denomination-item"
            >
              <div class="denomination-header">
                <span class="denomination-value">{{ coin.value }} F</span>
                <span class="denomination-icon">🪙</span>
              </div>
              <input 
                type="number" 
                v-model.number="coin.count" 
                @input="calculateTotal"
                min="0"
                class="count-input"
                placeholder="0"
              />
              <div class="denomination-total">
                {{ formatPrice(coin.value * coin.count) }}
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Total compté -->
      <div class="counting-summary">
        <div class="summary-row">
          <span>Total billets:</span>
          <span class="summary-value">{{ formatPrice(totalBills) }}</span>
        </div>
        <div class="summary-row">
          <span>Total pièces:</span>
          <span class="summary-value">{{ formatPrice(totalCoins) }}</span>
        </div>
        <div class="summary-row total-row">
          <span>Total compté:</span>
          <span class="summary-value highlight">{{ formatPrice(totalCounted) }}</span>
        </div>
      </div>

      <button class="btn-primary btn-full" @click="nextStep">
        Continuer →
      </button>
    </div>

    <!-- Étape 2: Vérification et écarts -->
    <div v-if="currentStep === 1" class="section-card">
      <h3>🔍 Vérification et Détection des Écarts</h3>
      <p class="section-description">Comparaison avec les montants attendus</p>

      <div class="verification-grid">
        <!-- Espèces -->
        <div class="verification-card">
          <div class="verification-header">
            <span class="verification-icon">💵</span>
            <h4>Espèces</h4>
          </div>
          <div class="verification-details">
            <div class="detail-row">
              <span>Attendu:</span>
              <span class="expected">{{ formatPrice(expected.cash) }}</span>
            </div>
            <div class="detail-row">
              <span>Compté:</span>
              <span class="counted">{{ formatPrice(totalCounted) }}</span>
            </div>
            <div class="detail-row variance">
              <span>Écart:</span>
              <span :class="['variance-value', getVarianceClass(cashVariance)]">
                {{ formatVariance(cashVariance) }}
              </span>
            </div>
          </div>
        </div>

        <!-- Carte bancaire -->
        <div class="verification-card">
          <div class="verification-header">
            <span class="verification-icon">💳</span>
            <h4>Carte Bancaire</h4>
          </div>
          <div class="verification-details">
            <div class="detail-row">
              <span>Attendu:</span>
              <span class="expected">{{ formatPrice(expected.card) }}</span>
            </div>
            <div class="detail-row">
              <span>TPE:</span>
              <span class="counted">{{ formatPrice(tpeTotal) }}</span>
            </div>
            <div class="detail-row variance">
              <span>Écart:</span>
              <span :class="['variance-value', getVarianceClass(cardVariance)]">
                {{ formatVariance(cardVariance) }}
              </span>
            </div>
          </div>
        </div>

        <!-- Mobile Money -->
        <div class="verification-card">
          <div class="verification-header">
            <span class="verification-icon">📱</span>
            <h4>Mobile Money</h4>
          </div>
          <div class="verification-details">
            <div class="detail-row">
              <span>Attendu:</span>
              <span class="expected">{{ formatPrice(expected.mobile) }}</span>
            </div>
            <div class="detail-row">
              <span>Confirmé:</span>
              <span class="counted">{{ formatPrice(mobileTotal) }}</span>
            </div>
            <div class="detail-row variance">
              <span>Écart:</span>
              <span :class="['variance-value', getVarianceClass(mobileVariance)]">
                {{ formatVariance(mobileVariance) }}
              </span>
            </div>
          </div>
        </div>

        <!-- Total général -->
        <div class="verification-card highlight">
          <div class="verification-header">
            <span class="verification-icon">💰</span>
            <h4>Total Général</h4>
          </div>
          <div class="verification-details">
            <div class="detail-row">
              <span>CA attendu:</span>
              <span class="expected">{{ formatPrice(totalExpected) }}</span>
            </div>
            <div class="detail-row">
              <span>CA réalisé:</span>
              <span class="counted">{{ formatPrice(totalRealized) }}</span>
            </div>
            <div class="detail-row variance">
              <span>Écart total:</span>
              <span :class="['variance-value', getVarianceClass(totalVariance)]">
                {{ formatVariance(totalVariance) }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- Justification si écart -->
      <div v-if="Math.abs(totalVariance) > 0" class="justification-section">
        <h4>📝 Justification de l'écart</h4>
        <textarea 
          v-model="justification"
          class="justification-textarea"
          placeholder="Veuillez expliquer l'écart constaté..."
          rows="4"
        ></textarea>
      </div>

      <div class="step-actions">
        <button class="btn-secondary" @click="prevStep">
          ← Retour
        </button>
        <button 
          class="btn-primary" 
          @click="nextStep"
          :disabled="Math.abs(totalVariance) > 0 && !justification.trim()"
        >
          Continuer →
        </button>
      </div>
    </div>

    <!-- Étape 3: Signature et validation -->
    <div v-if="currentStep === 2" class="section-card">
      <h3>✍️ Signature et Validation</h3>
      <p class="section-description">Validation finale par le responsable</p>

      <!-- Résumé de la journée -->
      <div class="daily-summary">
        <h4>📊 Résumé de la Journée</h4>
        <div class="summary-grid">
          <div class="summary-item">
            <span class="summary-label">Date</span>
            <span class="summary-value">{{ formatDate(new Date()) }}</span>
          </div>
          <div class="summary-item">
            <span class="summary-label">Caissier</span>
            <span class="summary-value">{{ cashierName }}</span>
          </div>
          <div class="summary-item">
            <span class="summary-label">Transactions</span>
            <span class="summary-value">{{ transactionCount }}</span>
          </div>
          <div class="summary-item">
            <span class="summary-label">CA Total</span>
            <span class="summary-value highlight">{{ formatPrice(totalRealized) }}</span>
          </div>
        </div>
      </div>

      <!-- Signature électronique -->
      <div class="signature-section">
        <h4>✍️ Signature Électronique</h4>
        <div class="signature-grid">
          <div class="signature-box">
            <label>Caissier</label>
            <div class="signature-field" :class="{ signed: signatures.cashier }">
              <span v-if="!signatures.cashier">Cliquez pour signer</span>
              <span v-else class="signature-text">{{ cashierName }}</span>
            </div>
            <button 
              v-if="!signatures.cashier"
              class="btn-sign"
              @click="signAsCashier"
            >
              ✍️ Signer
            </button>
          </div>

          <div class="signature-box">
            <label>Responsable</label>
            <div class="signature-field" :class="{ signed: signatures.manager }">
              <span v-if="!signatures.manager">En attente...</span>
              <span v-else class="signature-text">{{ managerName }}</span>
            </div>
            <button 
              v-if="!signatures.manager && signatures.cashier"
              class="btn-sign"
              @click="signAsManager"
            >
              ✍️ Signer
            </button>
          </div>
        </div>
      </div>

      <div class="step-actions">
        <button class="btn-secondary" @click="prevStep">
          ← Retour
        </button>
        <button 
          class="btn-primary" 
          @click="nextStep"
          :disabled="!signatures.cashier || !signatures.manager"
        >
          Continuer →
        </button>
      </div>
    </div>

    <!-- Étape 4: Rapport Z -->
    <div v-if="currentStep === 3" class="section-card">
      <h3>📋 Rapport Z de Clôture</h3>
      <p class="section-description">Aperçu du rapport de fin de journée</p>

      <div class="z-report">
        <div class="report-header">
          <h2>RAPPORT Z - CLÔTURE JOURNALIÈRE</h2>
          <div class="report-info">
            <p>Date: {{ formatDate(new Date()) }}</p>
            <p>Caisse N°: 001</p>
            <p>Caissier: {{ cashierName }}</p>
          </div>
        </div>

        <div class="report-section">
          <h4>CHIFFRE D'AFFAIRES</h4>
          <table class="report-table">
            <tr>
              <td>Espèces</td>
              <td class="amount">{{ formatPrice(expected.cash) }}</td>
            </tr>
            <tr>
              <td>Carte bancaire</td>
              <td class="amount">{{ formatPrice(expected.card) }}</td>
            </tr>
            <tr>
              <td>Mobile Money</td>
              <td class="amount">{{ formatPrice(expected.mobile) }}</td>
            </tr>
            <tr>
              <td>Carte cadeau</td>
              <td class="amount">{{ formatPrice(expected.gift) }}</td>
            </tr>
            <tr class="total-row">
              <td><strong>TOTAL CA</strong></td>
              <td class="amount"><strong>{{ formatPrice(totalExpected) }}</strong></td>
            </tr>
          </table>
        </div>

        <div class="report-section">
          <h4>STATISTIQUES</h4>
          <table class="report-table">
            <tr>
              <td>Nombre de transactions</td>
              <td>{{ transactionCount }}</td>
            </tr>
            <tr>
              <td>Nombre d'articles vendus</td>
              <td>{{ itemsSold }}</td>
            </tr>
            <tr>
              <td>Panier moyen</td>
              <td>{{ formatPrice(avgBasket) }}</td>
            </tr>
            <tr>
              <td>Temps moyen par transaction</td>
              <td>{{ avgTime }} min</td>
            </tr>
          </table>
        </div>

        <div class="report-section" v-if="Math.abs(totalVariance) > 0">
          <h4>ÉCARTS CONSTATÉS</h4>
          <table class="report-table">
            <tr>
              <td>Écart espèces</td>
              <td :class="['amount', getVarianceClass(cashVariance)]">
                {{ formatVariance(cashVariance) }}
              </td>
            </tr>
            <tr>
              <td>Justification</td>
              <td colspan="2">{{ justification }}</td>
            </tr>
          </table>
        </div>

        <div class="report-section">
          <h4>SIGNATURES</h4>
          <div class="signatures-display">
            <div>
              <p>Caissier: {{ cashierName }}</p>
              <p class="signature-time">{{ formatDateTime(new Date()) }}</p>
            </div>
            <div>
              <p>Responsable: {{ managerName }}</p>
              <p class="signature-time">{{ formatDateTime(new Date()) }}</p>
            </div>
          </div>
        </div>
      </div>

      <div class="step-actions">
        <button class="btn-secondary" @click="prevStep">
          ← Retour
        </button>
        <button class="btn-success btn-large" @click="finalizeClosing">
          🔒 Finaliser la Clôture
        </button>
      </div>
    </div>

    <!-- Modal de code responsable -->
    <div v-if="showPasswordModal" class="modal-overlay" @click.self="cancelPasswordModal">
      <div class="modal-content password-modal">
        <div class="modal-header">
          <h3>🔐 Validation Responsable</h3>
          <button class="close-btn" @click="cancelPasswordModal">×</button>
        </div>
        <div class="modal-body">
          <p>Veuillez saisir le code responsable pour valider la clôture</p>
          <input 
            type="password" 
            v-model="managerPassword"
            @keyup.enter="validateManagerPassword"
            placeholder="Code responsable"
            class="password-input"
            autofocus
          />
          <p class="password-hint">Code de démonstration: 1234</p>
        </div>
        <div class="modal-footer">
          <button class="btn-secondary" @click="cancelPasswordModal">Annuler</button>
          <button class="btn-primary" @click="validateManagerPassword">Valider</button>
        </div>
      </div>
    </div>

    <!-- Confirmation finale -->
    <div v-if="showSuccessModal" class="modal-overlay" @click.self="closeSuccessModal">
      <div class="modal-content success-modal">
        <div class="success-icon">✅</div>
        <h2>Clôture Réussie!</h2>
        <p>La caisse a été clôturée avec succès.</p>
        <p class="report-id">Rapport Z N°: {{ reportId }}</p>
        
        <div class="success-actions">
          <button class="btn-primary" @click="printZReport">
            🖨️ Imprimer Rapport Z
          </button>
          <button class="btn-secondary" @click="closeSuccessModal">
            Fermer
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CashierClosing',
  data() {
    return {
      currentStep: 0,
      closingStatus: 'in-progress',
      steps: [
        'Comptage',
        'Vérification',
        'Signature',
        'Rapport Z'
      ],
      bills: [
        { value: 10000, count: 0 },
        { value: 5000, count: 0 },
        { value: 2000, count: 0 },
        { value: 1000, count: 0 },
        { value: 500, count: 0 }
      ],
      coins: [
        { value: 500, count: 0 },
        { value: 200, count: 0 },
        { value: 100, count: 0 },
        { value: 50, count: 0 },
        { value: 25, count: 0 }
      ],
      expected: {
        cash: 1281375,
        card: 854250,
        mobile: 569500,
        gift: 142375
      },
      tpeTotal: 854250,
      mobileTotal: 569500,
      justification: '',
      signatures: {
        cashier: false,
        manager: false
      },
      cashierName: 'Marie K.',
      managerName: 'Amadou B.',
      transactionCount: 156,
      itemsSold: 827,
      avgBasket: 18254,
      avgTime: 3.2,
      showSuccessModal: false,
      showPasswordModal: false,
      managerPassword: '',
      reportId: ''
    };
  },
  computed: {
    totalBills() {
      return this.bills.reduce((sum, bill) => sum + (bill.value * bill.count), 0);
    },
    totalCoins() {
      return this.coins.reduce((sum, coin) => sum + (coin.value * coin.count), 0);
    },
    totalCounted() {
      return this.totalBills + this.totalCoins;
    },
    cashVariance() {
      return this.totalCounted - this.expected.cash;
    },
    cardVariance() {
      return this.tpeTotal - this.expected.card;
    },
    mobileVariance() {
      return this.mobileTotal - this.expected.mobile;
    },
    totalExpected() {
      return this.expected.cash + this.expected.card + this.expected.mobile + this.expected.gift;
    },
    totalRealized() {
      return this.totalCounted + this.tpeTotal + this.mobileTotal + this.expected.gift;
    },
    totalVariance() {
      return this.totalRealized - this.totalExpected;
    }
  },
  methods: {
    refreshData() {
      console.log('🔒 Données de clôture rafraîchies');
    },
    calculateTotal() {
      // Recalcul automatique via computed properties
    },
    nextStep() {
      if (this.currentStep < this.steps.length - 1) {
        this.currentStep++;
      }
    },
    prevStep() {
      if (this.currentStep > 0) {
        this.currentStep--;
      }
    },
    signAsCashier() {
      this.signatures.cashier = true;
    },
    signAsManager() {
      this.showPasswordModal = true;
    },
    validateManagerPassword() {
      if (this.managerPassword === '1234') {
        this.signatures.manager = true;
        this.showPasswordModal = false;
        this.managerPassword = '';
      } else {
        alert('❌ Code incorrect');
        this.managerPassword = '';
      }
    },
    cancelPasswordModal() {
      this.showPasswordModal = false;
      this.managerPassword = '';
    },
    finalizeClosing() {
      this.reportId = 'Z' + new Date().getFullYear() + 
                     String(new Date().getMonth() + 1).padStart(2, '0') + 
                     String(new Date().getDate()).padStart(2, '0') + 
                     '001';
      this.closingStatus = 'completed';
      this.showSuccessModal = true;
    },
    closeSuccessModal() {
      this.showSuccessModal = false;
      // Réinitialiser pour une nouvelle journée
      this.currentStep = 0;
      this.bills.forEach(b => b.count = 0);
      this.coins.forEach(c => c.count = 0);
      this.justification = '';
      this.signatures = { cashier: false, manager: false };
    },
    printZReport() {
      alert('🖨️ Impression du Rapport Z N°' + this.reportId + ' en cours...');
    },
    getStatusText() {
      const statuses = {
        'in-progress': 'En cours',
        'completed': 'Clôturée',
        'pending': 'En attente'
      };
      return statuses[this.closingStatus];
    },
    getVarianceClass(variance) {
      if (variance === 0) return 'neutral';
      return variance > 0 ? 'positive' : 'negative';
    },
    formatVariance(variance) {
      const sign = variance > 0 ? '+' : '';
      return sign + this.formatPrice(variance);
    },
    formatPrice(amount) {
      return new Intl.NumberFormat('fr-FR', {
        style: 'currency',
        currency: 'XOF',
        minimumFractionDigits: 0
      }).format(amount);
    },
    formatDate(date) {
      return new Intl.DateTimeFormat('fr-FR', {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      }).format(date);
    },
    formatDateTime(date) {
      return new Intl.DateTimeFormat('fr-FR', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
      }).format(date);
    }
  }
};
</script>

<style scoped>
.closing-content {
  padding: 20px 40px;
  max-width: 1400px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 32px;
}

.page-header h2 {
  font-size: 28px;
  font-weight: 700;
  color: #111827;
  margin-bottom: 8px;
}

.subtitle {
  color: #6b7280;
  font-size: 15px;
}

.closing-status {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 20px;
  background: white;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
}

.status-indicator {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  animation: pulse 2s infinite;
}

.status-indicator.in-progress {
  background: #f59e0b;
}

.status-indicator.completed {
  background: #10b981;
}

.status-text {
  font-size: 14px;
  font-weight: 600;
  color: #374151;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.steps-indicator {
  display: flex;
  justify-content: space-between;
  margin-bottom: 32px;
  position: relative;
}

.steps-indicator::before {
  content: '';
  position: absolute;
  top: 24px;
  left: 0;
  right: 0;
  height: 2px;
  background: #e5e7eb;
  z-index: 0;
}

.step {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  flex: 1;
  position: relative;
  z-index: 1;
}

.step-number {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: white;
  border: 2px solid #e5e7eb;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  font-weight: 700;
  color: #9ca3af;
  transition: all 0.3s ease;
}

.step.active .step-number {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  border-color: #3b82f6;
  color: white;
}

.step.completed .step-number {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  border-color: #10b981;
  color: white;
}

.step-label {
  font-size: 13px;
  font-weight: 600;
  color: #6b7280;
}

.step.active .step-label {
  color: #3b82f6;
}

.section-card {
  background: white;
  border-radius: 16px;
  padding: 32px;
  border: 1px solid #e5e7eb;
}

.section-card h3 {
  font-size: 22px;
  font-weight: 700;
  color: #111827;
  margin-bottom: 8px;
}

.section-description {
  color: #6b7280;
  font-size: 15px;
  margin-bottom: 32px;
}

.cash-counting {
  display: flex;
  flex-direction: column;
  gap: 32px;
  margin-bottom: 32px;
}

.denomination-group h4 {
  font-size: 16px;
  font-weight: 700;
  color: #111827;
  margin-bottom: 16px;
}

.denominations-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 16px;
}

.denomination-item {
  background: #f9fafb;
  border-radius: 12px;
  padding: 16px;
  border: 2px solid #e5e7eb;
  display: flex;
  flex-direction: column;
  gap: 12px;
  transition: border-color 0.2s ease;
}

.denomination-item:hover {
  border-color: #3b82f6;
}

.denomination-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.denomination-value {
  font-size: 14px;
  font-weight: 700;
  color: #111827;
}

.denomination-icon {
  font-size: 20px;
}

.count-input {
  width: 100%;
  padding: 10px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  text-align: center;
  color: #374151;
}

.count-input:focus {
  outline: none;
  border-color: #3b82f6;
}

.denomination-total {
  font-size: 14px;
  font-weight: 700;
  color: #10b981;
  text-align: center;
}

.counting-summary {
  background: #f9fafb;
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 24px;
}

.summary-row {
  display: flex;
  justify-content: space-between;
  padding: 12px 0;
  font-size: 15px;
  color: #374151;
  border-bottom: 1px solid #e5e7eb;
}

.summary-row:last-child {
  border-bottom: none;
}

.summary-row.total-row {
  padding-top: 16px;
  margin-top: 8px;
  border-top: 2px solid #e5e7eb;
  font-size: 18px;
  font-weight: 700;
}

.summary-value {
  font-weight: 700;
  color: #111827;
}

.summary-value.highlight {
  color: #10b981;
  font-size: 22px;
}

.verification-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  margin-bottom: 32px;
}

.verification-card {
  background: #f9fafb;
  border-radius: 12px;
  padding: 24px;
  border: 2px solid #e5e7eb;
}

.verification-card.highlight {
  background: linear-gradient(135deg, #dbeafe 0%, #eff6ff 100%);
  border-color: #3b82f6;
}

.verification-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 20px;
}

.verification-icon {
  font-size: 28px;
}

.verification-header h4 {
  font-size: 16px;
  font-weight: 700;
  color: #111827;
}

.verification-details {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  font-size: 14px;
  color: #374151;
}

.detail-row.variance {
  padding-top: 12px;
  margin-top: 8px;
  border-top: 2px solid #e5e7eb;
  font-weight: 700;
}

.expected {
  color: #6b7280;
  font-weight: 600;
}

.counted {
  color: #111827;
  font-weight: 700;
}

.variance-value {
  font-weight: 800;
  font-size: 16px;
}

.variance-value.neutral {
  color: #10b981;
}

.variance-value.positive {
  color: #10b981;
}

.variance-value.negative {
  color: #ef4444;
}

.justification-section {
  margin-top: 32px;
  padding: 24px;
  background: #fef3c7;
  border-radius: 12px;
  border: 2px solid #f59e0b;
}

.justification-section h4 {
  font-size: 16px;
  font-weight: 700;
  color: #92400e;
  margin-bottom: 16px;
}

.justification-textarea {
  width: 100%;
  padding: 14px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  font-size: 14px;
  font-family: inherit;
  resize: vertical;
}

.justification-textarea:focus {
  outline: none;
  border-color: #f59e0b;
}

.step-actions {
  display: flex;
  gap: 16px;
  margin-top: 32px;
}

.btn-full {
  width: 100%;
}

.btn-large {
  padding: 16px 32px;
  font-size: 16px;
}

.daily-summary {
  background: #f9fafb;
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 32px;
}

.daily-summary h4 {
  font-size: 16px;
  font-weight: 700;
  color: #111827;
  margin-bottom: 20px;
}

.summary-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
}

.summary-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.summary-label {
  font-size: 12px;
  color: #6b7280;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.summary-item .summary-value {
  font-size: 16px;
  font-weight: 700;
  color: #111827;
}

.signature-section {
  margin-bottom: 32px;
}

.signature-section h4 {
  font-size: 16px;
  font-weight: 700;
  color: #111827;
  margin-bottom: 20px;
}

.signature-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
}

.signature-box label {
  display: block;
  font-size: 13px;
  font-weight: 600;
  color: #374151;
  margin-bottom: 12px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.signature-field {
  min-height: 100px;
  border: 2px dashed #e5e7eb;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 12px;
  background: #f9fafb;
  color: #9ca3af;
  font-style: italic;
}

.signature-field.signed {
  border-color: #10b981;
  background: #dcfce7;
  border-style: solid;
}

.signature-text {
  font-size: 24px;
  font-weight: 700;
  color: #166534;
  font-family: 'Brush Script MT', cursive;
}

.btn-sign {
  width: 100%;
  padding: 12px;
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 15px;
  font-weight: 700;
  cursor: pointer;
  transition: transform 0.2s ease;
}

.btn-sign:hover {
  transform: translateY(-2px);
}

.z-report {
  background: white;
  border: 2px solid #374151;
  border-radius: 8px;
  padding: 32px;
  font-family: 'Courier New', monospace;
  margin-bottom: 32px;
}

.report-header {
  text-align: center;
  margin-bottom: 32px;
  padding-bottom: 20px;
  border-bottom: 2px solid #374151;
}

.report-header h2 {
  font-size: 20px;
  font-weight: 700;
  margin-bottom: 16px;
}

.report-info p {
  font-size: 13px;
  margin: 4px 0;
}

.report-section {
  margin-bottom: 24px;
  padding-bottom: 20px;
  border-bottom: 1px solid #e5e7eb;
}

.report-section:last-of-type {
  border-bottom: none;
}

.report-section h4 {
  font-size: 14px;
  font-weight: 700;
  margin-bottom: 12px;
  color: #374151;
}

.report-table {
  width: 100%;
  font-size: 13px;
}

.report-table tr {
  line-height: 1.8;
}

.report-table td {
  padding: 4px 0;
}

.report-table td.amount {
  text-align: right;
}

.report-table tr.total-row {
  border-top: 2px solid #374151;
  border-bottom: 2px solid #374151;
}

.signatures-display {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
  margin-top: 16px;
}

.signature-time {
  font-size: 11px;
  color: #6b7280;
  margin-top: 4px;
}

.success-modal {
  text-align: center;
}

.success-icon {
  font-size: 64px;
  margin-bottom: 20px;
}

.success-modal h2 {
  font-size: 28px;
  font-weight: 700;
  color: #111827;
  margin-bottom: 12px;
}

.success-modal p {
  color: #6b7280;
  font-size: 15px;
  margin-bottom: 8px;
}

.report-id {
  font-family: 'Courier New', monospace;
  font-weight: 700;
  color: #3b82f6;
  font-size: 16px;
  margin-top: 16px;
  margin-bottom: 32px;
}

.success-actions {
  display: flex;
  gap: 12px;
  justify-content: center;
}

.btn-success {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  border: none;
}

.btn-success:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(16, 185, 129, 0.3);
}

.password-modal {
  max-width: 450px;
}

.password-input {
  width: 100%;
  padding: 14px 16px;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  text-align: center;
  margin: 16px 0;
  letter-spacing: 4px;
}

.password-input:focus {
  outline: none;
  border-color: #3b82f6;
}

.password-hint {
  font-size: 12px;
  color: #6b7280;
  font-style: italic;
  text-align: center;
}
</style>