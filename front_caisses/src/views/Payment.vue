<template>
  <div class="payment-content">
    <div class="payment-layout">
      <!-- Section gauche: Récapitulatif de la commande -->
      <div class="payment-left">
        <div class="order-summary">
          <h2>📋 Récapitulatif de la commande</h2>
          
          <div class="order-items">
            <div v-for="item in orderItems" :key="item.id" class="order-item">
              <div class="item-info">
                <span class="item-name">{{ item.nom }}</span>
                <span class="item-quantity">x{{ item.quantity }}</span>
              </div>
              <span class="item-price">{{ formatPrice(item.prix_unitaire * item.quantity) }}</span>
            </div>
          </div>

          <div class="order-totals">
            <div class="total-row">
              <span>Sous-total</span>
              <span>{{ formatPrice(subtotal) }}</span>
            </div>
            <div class="total-row" v-if="discount > 0">
              <span>Remise</span>
              <span class="discount-amount">-{{ formatPrice(discount) }}</span>
            </div>
            <div class="total-row">
              <span>TVA (18%)</span>
              <span>{{ formatPrice(tax) }}</span>
            </div>
            <div class="total-row grand-total">
              <span>TOTAL À PAYER</span>
              <span>{{ formatPrice(total) }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Section droite: Méthodes de paiement -->
      <div class="payment-right">
        <h2>💳 Méthode de paiement</h2>
        
        <div class="payment-methods">
          <button
            v-for="method in paymentMethods"
            :key="method.id"
            :class="['payment-method-btn', { active: selectedMethod === method.id }]"
            @click="selectPaymentMethod(method.id)"
          >
            <span class="method-icon">{{ method.icon }}</span>
            <div class="method-info">
              <span class="method-name">{{ method.name }}</span>
              <span class="method-desc">{{ method.description }}</span>
            </div>
          </button>
        </div>

        <!-- Formulaire de paiement en espèces -->
        <div v-if="selectedMethod === 'cash'" class="payment-form">
          <h3>💵 Paiement en espèces</h3>
          <div class="form-group">
            <label>Montant reçu</label>
            <input
              type="number"
              v-model.number="cashReceived"
              class="input input-lg"
              placeholder="Entrez le montant reçu"
              @input="calculateChange"
            >
          </div>
          
          <div class="quick-amounts">
            <button
              v-for="amount in quickCashAmounts"
              :key="amount"
              class="quick-amount-btn"
              @click="cashReceived = amount; calculateChange()"
            >
              {{ formatPrice(amount) }}
            </button>
          </div>

          <div v-if="change >= 0 && cashReceived > 0" class="change-display">
            <div class="change-label">Monnaie à rendre</div>
            <div class="change-amount">{{ formatPrice(change) }}</div>
          </div>

          <div v-if="cashReceived > 0 && cashReceived < total" class="error-message">
            ⚠️ Montant insuffisant
          </div>
        </div>

        <!-- Formulaire de paiement par carte -->
        <div v-if="selectedMethod === 'card'" class="payment-form">
          <h3>💳 Paiement par carte bancaire</h3>
          <div class="card-simulation">
            <div class="tpe-display">
              <div class="tpe-screen">
                <div class="tpe-text">{{ tpeMessage }}</div>
                <div class="tpe-amount">{{ formatPrice(total) }}</div>
              </div>
              <button class="btn btn-primary btn-full" @click="simulateCardPayment">
                {{ tpeButtonText }}
              </button>
            </div>
          </div>
        </div>

        <!-- Paiement Mobile Money -->
        <div v-if="selectedMethod === 'mobile'" class="payment-form">
          <h3>📱 Mobile Money</h3>
          <div class="mobile-money-form">
            <div class="form-group">
              <label>Opérateur</label>
              <select v-model="mobileOperator" class="input">
                <option value="mtn">MTN Mobile Money</option>
                <option value="moov">Moov Money</option>
                <option value="orange">Orange Money</option>
              </select>
            </div>
            <div class="form-group">
              <label>Numéro de téléphone</label>
              <input
                type="tel"
                v-model="mobilePhone"
                class="input"
                placeholder="Ex: 0701234567"
              >
            </div>
            <div class="qr-code-display">
              <div class="qr-placeholder">
                <div class="qr-icon">📱</div>
                <p>QR Code pour paiement</p>
                <p class="qr-amount">{{ formatPrice(total) }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Paiement par carte cadeau -->
        <div v-if="selectedMethod === 'gift'" class="payment-form">
          <h3>🎁 Carte cadeau</h3>
          <div class="form-group">
            <label>Numéro de carte cadeau</label>
            <input
              type="text"
              v-model="giftCardNumber"
              class="input"
              placeholder="XXXX-XXXX-XXXX-XXXX"
            >
          </div>
          <div v-if="giftCardBalance > 0" class="gift-card-balance">
            <span>Solde disponible:</span>
            <span class="balance-amount">{{ formatPrice(giftCardBalance) }}</span>
          </div>
        </div>

        <!-- Paiement fractionné -->
        <div v-if="selectedMethod === 'split'" class="payment-form">
          <h3>💰 Paiement fractionné</h3>
          <div class="split-payments">
            <div v-for="(split, index) in splitPayments" :key="index" class="split-item">
              <select v-model="split.method" class="input">
                <option value="cash">Espèces</option>
                <option value="card">Carte</option>
                <option value="mobile">Mobile Money</option>
              </select>
              <input
                type="number"
                v-model.number="split.amount"
                class="input"
                placeholder="Montant"
              >
              <button class="btn-danger-sm" @click="removeSplitPayment(index)">×</button>
            </div>
            <button class="btn-secondary" @click="addSplitPayment">
              + Ajouter un paiement
            </button>
          </div>
          <div class="split-summary">
            <div class="split-row">
              <span>Total payé:</span>
              <span>{{ formatPrice(totalSplitAmount) }}</span>
            </div>
            <div class="split-row">
              <span>Reste à payer:</span>
              <span :class="{ 'text-danger': remainingSplitAmount > 0 }">
                {{ formatPrice(remainingSplitAmount) }}
              </span>
            </div>
          </div>
        </div>

        <!-- Boutons d'action -->
        <div class="payment-actions">
          <button class="btn btn-secondary btn-full" @click="cancelPayment">
            ← Retour au panier
          </button>
          <button
            class="btn btn-primary btn-full"
            @click="processPayment"
            :disabled="!canProcessPayment"
          >
            ✅ Valider le paiement
          </button>
        </div>
      </div>
    </div>

    <!-- Modal de confirmation -->
    <div v-if="showConfirmModal" class="modal-overlay" @click.self="closeConfirmModal">
      <div class="modal-content modal-sm">
        <div class="modal-header success">
          <div class="success-icon">✅</div>
          <h3>Paiement réussi !</h3>
        </div>
        <div class="modal-body">
          <div class="payment-receipt">
            <div class="receipt-row">
              <span>Montant total:</span>
              <span class="receipt-value">{{ formatPrice(total) }}</span>
            </div>
            <div class="receipt-row">
              <span>Méthode:</span>
              <span class="receipt-value">{{ getMethodName(selectedMethod) }}</span>
            </div>
            <div class="receipt-row" v-if="selectedMethod === 'cash'">
              <span>Montant reçu:</span>
              <span class="receipt-value">{{ formatPrice(cashReceived) }}</span>
            </div>
            <div class="receipt-row" v-if="selectedMethod === 'cash'">
              <span>Monnaie rendue:</span>
              <span class="receipt-value">{{ formatPrice(change) }}</span>
            </div>
            <div class="receipt-row">
              <span>Transaction #:</span>
              <span class="receipt-value">{{ transactionId }}</span>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn btn-secondary" @click="printReceipt">
            🖨️ Imprimer ticket
          </button>
          <button class="btn btn-primary" @click="newTransaction">
            ✨ Nouvelle vente
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PaymentView',
  data() {
    return {
      // Données de commande mockées
      orderItems: [
        { id: 1, nom: 'Coca-Cola 1.5L', prix_unitaire: 1200, quantity: 2 },
        { id: 2, nom: 'Pain de mie', prix_unitaire: 800, quantity: 1 },
        { id: 3, nom: 'Lait NIDO 400g', prix_unitaire: 3500, quantity: 1 },
      ],
      discount: 500,
      
      // Méthodes de paiement
      paymentMethods: [
        { id: 'cash', name: 'Espèces', icon: '💵', description: 'Paiement en liquide' },
        { id: 'card', name: 'Carte bancaire', icon: '💳', description: 'CB, Visa, Mastercard' },
        { id: 'mobile', name: 'Mobile Money', icon: '📱', description: 'MTN, Moov, Orange' },
        { id: 'gift', name: 'Carte cadeau', icon: '🎁', description: 'Chèque cadeau' },
        { id: 'split', name: 'Paiement fractionné', icon: '💰', description: 'Multiple méthodes' },
      ],
      
      selectedMethod: 'cash',
      
      // Paiement en espèces
      cashReceived: 0,
      quickCashAmounts: [5000, 10000, 20000, 50000],
      
      // Paiement par carte
      tpeMessage: 'Insérez ou tapez la carte',
      tpeButtonText: 'Simuler paiement',
      cardProcessing: false,
      
      // Mobile Money
      mobileOperator: 'mtn',
      mobilePhone: '',
      
      // Carte cadeau
      giftCardNumber: '',
      giftCardBalance: 15000,
      
      // Paiement fractionné
      splitPayments: [
        { method: 'cash', amount: 0 },
        { method: 'card', amount: 0 },
      ],
      
      // Modal
      showConfirmModal: false,
      transactionId: '',
    };
  },
  computed: {
    subtotal() {
      return this.orderItems.reduce((sum, item) => sum + (item.prix_unitaire * item.quantity), 0);
    },
    tax() {
      return (this.subtotal - this.discount) * 0.18;
    },
    total() {
      return this.subtotal - this.discount + this.tax;
    },
    change() {
      return this.cashReceived - this.total;
    },
    totalSplitAmount() {
      return this.splitPayments.reduce((sum, split) => sum + (split.amount || 0), 0);
    },
    remainingSplitAmount() {
      return this.total - this.totalSplitAmount;
    },
    canProcessPayment() {
      if (this.selectedMethod === 'cash') {
        return this.cashReceived >= this.total;
      } else if (this.selectedMethod === 'split') {
        return this.remainingSplitAmount <= 0;
      }
      return true;
    }
  },
  methods: {
    refreshData() {
      console.log('💳 Payment rafraîchi');
    },
    selectPaymentMethod(methodId) {
      this.selectedMethod = methodId;
      this.resetPaymentForms();
    },
    resetPaymentForms() {
      this.cashReceived = 0;
      this.tpeMessage = 'Insérez ou tapez la carte';
      this.tpeButtonText = 'Simuler paiement';
      this.mobilePhone = '';
      this.giftCardNumber = '';
    },
    calculateChange() {
      // La monnaie est calculée automatiquement via computed
    },
    simulateCardPayment() {
      this.cardProcessing = true;
      this.tpeMessage = 'Traitement en cours...';
      this.tpeButtonText = 'Patientez...';
      
      setTimeout(() => {
        this.tpeMessage = '✅ Paiement accepté';
        this.tpeButtonText = 'Paiement réussi';
        this.cardProcessing = false;
      }, 2000);
    },
    addSplitPayment() {
      this.splitPayments.push({ method: 'cash', amount: 0 });
    },
    removeSplitPayment(index) {
      this.splitPayments.splice(index, 1);
    },
    processPayment() {
      // Générer un ID de transaction
      this.transactionId = 'TRX' + Date.now();
      
      // Afficher la confirmation
      this.showConfirmModal = true;
      
      // Log pour debug
      console.log('💳 Paiement traité:', {
        method: this.selectedMethod,
        total: this.total,
        transactionId: this.transactionId
      });
    },
    cancelPayment() {
      if (confirm('Annuler le paiement et retourner au panier ?')) {
        alert('← Retour au point de vente');
      }
    },
    closeConfirmModal() {
      this.showConfirmModal = false;
    },
    printReceipt() {
      alert('🖨️ Impression du ticket...\n(Fonctionnalité à intégrer avec Electron)');
    },
    newTransaction() {
      this.showConfirmModal = false;
      this.resetPaymentForms();
      this.selectedMethod = 'cash';
      alert('✨ Nouvelle vente - Retour au point de vente');
    },
    getMethodName(methodId) {
      const method = this.paymentMethods.find(m => m.id === methodId);
      return method ? method.name : '';
    },
    formatPrice(amount) {
      return new Intl.NumberFormat('fr-FR', {
        style: 'currency',
        currency: 'XOF',
        minimumFractionDigits: 0
      }).format(amount);
    }
  }
};
</script>

<style scoped>
.payment-content {
  padding: 20px;
  height: calc(100vh - 160px);
}

.payment-layout {
  display: grid;
  grid-template-columns: 400px 1fr;
  gap: 24px;
  height: 100%;
}

/* Section gauche */
.payment-left {
  background: white;
  border-radius: 16px;
  padding: 24px;
  border: 1px solid #e5e7eb;
  overflow-y: auto;
}

.order-summary h2 {
  font-size: 20px;
  font-weight: 700;
  color: #111827;
  margin-bottom: 20px;
}

.order-items {
  margin-bottom: 24px;
}

.order-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid #f3f4f6;
}

.item-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.item-name {
  font-size: 14px;
  font-weight: 600;
  color: #111827;
}

.item-quantity {
  font-size: 12px;
  color: #6b7280;
}

.item-price {
  font-size: 15px;
  font-weight: 700;
  color: #10b981;
}

.order-totals {
  background: #f9fafb;
  padding: 16px;
  border-radius: 12px;
}

.total-row {
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
  font-size: 14px;
  color: #374151;
}

.discount-amount {
  color: #10b981;
  font-weight: 600;
}

.grand-total {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 2px solid #e5e7eb;
  font-size: 18px;
  font-weight: 700;
  color: #111827;
}

.grand-total span:last-child {
  font-size: 24px;
  color: #10b981;
}

/* Section droite */
.payment-right {
  background: white;
  border-radius: 16px;
  padding: 24px;
  border: 1px solid #e5e7eb;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
}

.payment-right h2 {
  font-size: 20px;
  font-weight: 700;
  color: #111827;
  margin-bottom: 20px;
}

.payment-methods {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 12px;
  margin-bottom: 24px;
}

.payment-method-btn {
  padding: 16px;
  background: white;
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 12px;
  text-align: left;
}

.payment-method-btn:hover {
  border-color: #3b82f6;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.15);
}

.payment-method-btn.active {
  border-color: #10b981;
  background: #ecfdf5;
}

.method-icon {
  font-size: 32px;
}

.method-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.method-name {
  font-size: 14px;
  font-weight: 700;
  color: #111827;
}

.method-desc {
  font-size: 12px;
  color: #6b7280;
}

.payment-form {
  flex: 1;
  margin-bottom: 20px;
}

.payment-form h3 {
  font-size: 18px;
  font-weight: 700;
  color: #111827;
  margin-bottom: 16px;
}

.form-group {
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  font-size: 13px;
  font-weight: 600;
  color: #374151;
  margin-bottom: 8px;
}

.input-lg {
  font-size: 18px;
  font-weight: 700;
  text-align: center;
}

.quick-amounts {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 8px;
  margin-bottom: 20px;
}

.quick-amount-btn {
  padding: 12px;
  background: #f3f4f6;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.quick-amount-btn:hover {
  background: #10b981;
  color: white;
  border-color: #10b981;
}

.change-display {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  padding: 20px;
  border-radius: 12px;
  text-align: center;
  margin-bottom: 16px;
}

.change-label {
  font-size: 13px;
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: 8px;
}

.change-amount {
  font-size: 32px;
  font-weight: 800;
  color: white;
}

.error-message {
  padding: 12px;
  background: #fee2e2;
  border: 1px solid #fecaca;
  border-radius: 8px;
  color: #dc2626;
  font-size: 14px;
  font-weight: 600;
  text-align: center;
}

.tpe-display {
  background: #1f2937;
  padding: 24px;
  border-radius: 12px;
}

.tpe-screen {
  background: #4ade80;
  padding: 24px;
  border-radius: 8px;
  text-align: center;
  margin-bottom: 16px;
}

.tpe-text {
  font-size: 14px;
  color: #065f46;
  font-weight: 600;
  margin-bottom: 12px;
}

.tpe-amount {
  font-size: 28px;
  font-weight: 800;
  color: #065f46;
}

.qr-code-display {
  margin-top: 20px;
}

.qr-placeholder {
  width: 200px;
  height: 200px;
  margin: 0 auto;
  background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%);
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border: 2px dashed #d1d5db;
}

.qr-icon {
  font-size: 48px;
  margin-bottom: 12px;
}

.qr-amount {
  font-size: 18px;
  font-weight: 700;
  color: #10b981;
  margin-top: 8px;
}

.gift-card-balance {
  padding: 16px;
  background: #ecfdf5;
  border-radius: 8px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 12px;
}

.balance-amount {
  font-size: 20px;
  font-weight: 700;
  color: #10b981;
}

.split-payments {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 20px;
}

.split-item {
  display: grid;
  grid-template-columns: 1fr 1fr auto;
  gap: 8px;
}

.split-summary {
  background: #f9fafb;
  padding: 16px;
  border-radius: 8px;
}

.split-row {
  display: flex;
  justify-content: space-between;
  padding: 6px 0;
  font-size: 15px;
  font-weight: 600;
}

.text-danger {
  color: #dc2626;
}

.payment-actions {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  padding-top: 20px;
  border-top: 2px solid #e5e7eb;
}

.btn-full {
  padding: 14px 24px;
  font-size: 15px;
  font-weight: 700;
}

/* Modal */
.modal-header.success {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.success-icon {
  width: 64px;
  height: 64px;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32px;
}

.payment-receipt {
  background: #f9fafb;
  padding: 20px;
  border-radius: 12px;
}

.receipt-row {
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
  font-size: 14px;
}

.receipt-value {
  font-weight: 700;
  color: #111827;
}
</style>