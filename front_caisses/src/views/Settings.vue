<template>
  <div class="settings-content">
    <div class="settings-card">
      <div class="settings-header">
        <h2>⚙️ Paramètres</h2>
        <p>Configuration du module de gestion des caisses</p>
      </div>

      <div class="settings-section">
        <h3>Informations du caissier</h3>
        <div class="info-grid">
          <div class="info-item">
            <span class="info-label">Nom complet</span>
            <span class="info-value">Caissier 01</span>
          </div>
          <div class="info-item">
            <span class="info-label">Matricule</span>
            <span class="info-value">CAISSE-001</span>
          </div>
          <div class="info-item">
            <span class="info-label">Caisse assignée</span>
            <span class="info-value">Caisse principale #1</span>
          </div>
          <div class="info-item">
            <span class="info-label">Statut</span>
            <span class="badge badge-success">Actif</span>
          </div>
        </div>
      </div>

      <div class="settings-section">
        <h3>Préférences</h3>
        <div class="preferences-list">
          <div class="preference-item">
            <div class="preference-info">
              <span class="preference-label">Son des bips</span>
              <span class="preference-desc">Activer le son lors du scan de produits</span>
            </div>
            <label class="toggle">
              <input type="checkbox" checked>
              <span class="slider"></span>
            </label>
          </div>
          <div class="preference-item">
            <div class="preference-info">
              <span class="preference-label">Impression automatique</span>
              <span class="preference-desc">Imprimer automatiquement le ticket après paiement</span>
            </div>
            <label class="toggle">
              <input type="checkbox" checked>
              <span class="slider"></span>
            </label>
          </div>
          <div class="preference-item">
            <div class="preference-info">
              <span class="preference-label">Thème sombre</span>
              <span class="preference-desc">Activer le mode sombre de l'interface</span>
            </div>
            <label class="toggle">
              <input type="checkbox">
              <span class="slider"></span>
            </label>
          </div>
        </div>
      </div>

      <div class="settings-section">
        <h3>À propos</h3>
        <div class="about-info">
          <p><strong>Module:</strong> Gestion des Caisses</p>
          <p><strong>Version:</strong> 1.0.0</p>
          <p><strong>Développé par:</strong> ExpressMall Team</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SettingsView',
  methods: {
    refreshData() {
      console.log('⚙️ Paramètres rafraîchis');
    }
  }
};
</script>

<style scoped>
.settings-content {
  padding: 20px 40px;
}

.settings-card {
  background: white;
  border-radius: 16px;
  padding: 32px;
  border: 1px solid #e5e7eb;
}

.settings-header {
  margin-bottom: 32px;
  padding-bottom: 24px;
  border-bottom: 2px solid #e5e7eb;
}

.settings-header h2 {
  font-size: 28px;
  font-weight: 700;
  color: #111827;
  margin-bottom: 8px;
}

.settings-header p {
  color: #6b7280;
  font-size: 15px;
}

.settings-section {
  margin-bottom: 32px;
}

.settings-section h3 {
  font-size: 18px;
  font-weight: 700;
  color: #111827;
  margin-bottom: 20px;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.info-label {
  font-size: 13px;
  font-weight: 600;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.info-value {
  font-size: 16px;
  font-weight: 600;
  color: #111827;
}

.preferences-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.preference-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  background: #f9fafb;
  border-radius: 12px;
  border: 1px solid #e5e7eb;
}

.preference-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.preference-label {
  font-size: 15px;
  font-weight: 600;
  color: #111827;
}

.preference-desc {
  font-size: 13px;
  color: #6b7280;
}

.toggle {
  position: relative;
  display: inline-block;
  width: 52px;
  height: 28px;
}

.toggle input {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #e5e7eb;
  transition: 0.3s;
  border-radius: 34px;
}

.slider:before {
  position: absolute;
  content: "";
  height: 20px;
  width: 20px;
  left: 4px;
  bottom: 4px;
  background-color: white;
  transition: 0.3s;
  border-radius: 50%;
}

input:checked + .slider {
  background-color: #10b981;
}

input:checked + .slider:before {
  transform: translateX(24px);
}

.about-info p {
  margin-bottom: 12px;
  color: #374151;
  font-size: 14px;
}
</style>