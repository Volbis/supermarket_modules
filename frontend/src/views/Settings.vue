<template>
  <div class="settings-container">
    <!-- Content -->
    <div class="settings-content">
      <!-- Navigation tabs -->
      <div class="settings-sidebar">
        <button 
          v-for="tab in tabs" 
          :key="tab.id"
          :class="['settings-tab', { active: activeTab === tab.id }]"
          @click="activeTab = tab.id"
        >
          <span class="tab-icon">{{ tab.icon }}</span>
          <span>{{ tab.label }}</span>
        </button>
      </div>

      <!-- Content area -->
      <div class="settings-main">
        <!-- Profil utilisateur -->
        <div v-if="activeTab === 'profile'" class="settings-section">
          <h2 class="section-title">Informations du profil</h2>
          
          <div class="profile-card">
            <div class="profile-avatar-section">
              <div class="profile-avatar-large">
                <img v-if="userProfile.image" :src="userProfile.image" alt="avatar" style="width:100%;height:100%;border-radius:50%;" />
                <span v-else>{{ userInitials }}</span>
              </div>
              <div>
                <button class="btn-secondary" @click="selectPhoto">Changer la photo</button>
                <p class="helper-text">JPG, PNG. Max 2MB</p>
                <!-- Input fichier invisible -->
                <input 
                  type="file" 
                  ref="fileInput" 
                  accept="image/*" 
                  style="display: none" 
                  @change="onFileSelected"
                />
              </div>
            </div>

            <div class="form-group">
              <label>Nom complet</label>
              <input type="text" v-model="userProfile.name" class="form-input" />
            </div>

            <div class="form-group">
              <label>Email</label>
              <input type="email" v-model="userProfile.email" class="form-input" />
            </div>

            <div class="form-group">
              <label>Téléphone</label>
              <input type="tel" v-model="userProfile.phone" class="form-input" />
            </div>

            <div class="form-group">
              <label>Rôle</label>
              <input type="text" v-model="userProfile.role" class="form-input" disabled />
            </div>

            <div class="form-actions">
              <button class="btn-primary" @click="saveProfile">Enregistrer les modifications</button>
              <button class="btn-secondary">Annuler</button>
            </div>
          </div>
        </div>

        <!-- Paramètres de l'application -->
        <div v-if="activeTab === 'app'" class="settings-section">
          <h2 class="section-title">Paramètres de l'application</h2>
          
          <div class="settings-card">
            <div class="setting-item">
              <div class="setting-info">
                <h4>Mode sombre</h4>
                <p>Activer le thème sombre de l'application</p>
              </div>
              <label class="toggle-switch">
                <input type="checkbox" v-model="appSettings.darkMode" />
                <span class="toggle-slider"></span>
              </label>
            </div>

            <div class="setting-item">
              <div class="setting-info">
                <h4>Notifications</h4>
                <p>Recevoir des notifications pour les activités importantes</p>
              </div>
              <label class="toggle-switch">
                <input type="checkbox" v-model="appSettings.notifications" />
                <span class="toggle-slider"></span>
              </label>
            </div>

            <div class="setting-item">
              <div class="setting-info">
                <h4>Notifications sonores</h4>
                <p>Jouer un son lors de nouvelles notifications</p>
              </div>
              <label class="toggle-switch">
                <input type="checkbox" v-model="appSettings.soundNotifications" />
                <span class="toggle-slider"></span>
              </label>
            </div>

            <div class="setting-item">
              <div class="setting-info">
                <h4>Langue</h4>
                <p>Choisir la langue de l'interface</p>
              </div>
              <select v-model="appSettings.language" class="form-select">
                <option value="fr">Français</option>
                <option value="en">English</option>
              </select>
            </div>
          </div>
        </div>

        <!-- Sécurité -->
        <div v-if="activeTab === 'security'" class="settings-section">
          <h2 class="section-title">Sécurité et confidentialité</h2>
          
          <div class="settings-card">
            <h3 class="card-subtitle">Changer le mot de passe</h3>
            
            <div class="form-group">
              <label>Mot de passe actuel</label>
              <input type="password" v-model="security.currentPassword" class="form-input" />
            </div>

            <div class="form-group">
              <label>Nouveau mot de passe</label>
              <input type="password" v-model="security.newPassword" class="form-input" />
            </div>

            <div class="form-group">
              <label>Confirmer le mot de passe</label>
              <input type="password" v-model="security.confirmPassword" class="form-input" />
            </div>

            <button class="btn-primary" @click="changePassword">Changer le mot de passe</button>
          </div>

          <div class="settings-card danger-zone">
            <h3 class="card-subtitle">Zone de danger</h3>
            <p>Actions irréversibles sur votre compte</p>
            <button class="btn-danger">Supprimer le compte</button>
          </div>
        </div>

        <!-- À propos -->
        <div v-if="activeTab === 'about'" class="settings-section">
          <h2 class="section-title">À propos</h2>
          
          <div class="settings-card">
            <div class="about-item">
              <span class="about-label">Version</span>
              <span class="about-value">1.0.0</span>
            </div>
            <div class="about-item">
              <span class="about-label">Dernière mise à jour</span>
              <span class="about-value">21 Octobre 2025</span>
            </div>
            <div class="about-item">
              <span class="about-label">Développé par</span>
              <span class="about-value">Équipe ExpressMall</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SettingsView',
  data() {
    return {
      activeTab: 'profile',
      tabs: [
        { id: 'profile', label: 'Profil', icon: '👤' },
        { id: 'app', label: 'Application', icon: '⚙️' },
        { id: 'security', label: 'Sécurité', icon: '🔒' },
        { id: 'about', label: 'À propos', icon: 'ℹ️' }
      ],
      userProfile: {
        name: 'Déric EZIN',
        email: 'deric.ezin@expressmail.com',
        phone: '+225 XX XX XX XX XX',
        role: 'Administrateur',
        image: null
      },
      appSettings: {
        darkMode: false,
        notifications: true,
        soundNotifications: false,
        language: 'fr'
      },
      security: {
        currentPassword: '',
        newPassword: '',
        confirmPassword: ''
      }
    }
  },
  computed: {
    userInitials() {
      return this.userProfile.name
        .split(' ')
        .map(n => n[0])
        .join('')
        .toUpperCase()
    }
  },
  methods: {
    // === MÉTHODE PUBLIQUE POUR REFRESH DEPUIS APP.VUE ===
    refreshData() {
      console.log('ℹ️ Settings n\'a pas besoin de refresh (page statique)');
    },
    
    saveProfile() {
      console.log('Profil sauvegardé', this.userProfile)
      alert('Profil mis à jour avec succès !')
    },
    changePassword() {
      if (this.security.newPassword !== this.security.confirmPassword) {
        alert('Les mots de passe ne correspondent pas')
        return
      }
      console.log('Mot de passe changé')
      alert('Mot de passe changé avec succès !')
      this.security = {
        currentPassword: '',
        newPassword: '',
        confirmPassword: ''
      }
    },

    // ==================== PHOTO ====================
    selectPhoto() {
      this.$refs.fileInput.click()
    },
    onFileSelected(event) {
      const file = event.target.files[0]
      if (!file) return
      if (file.size > 2 * 1024 * 1024) {
        alert('Le fichier est trop volumineux (max 2MB)')
        return
      }
      const reader = new FileReader()
      reader.onload = e => {
        this.userProfile.image = e.target.result
      }
      reader.readAsDataURL(file)
    }
  }
}
</script>

<style scoped>
/* ==================== CONTAINER ==================== */
.settings-container {
  background-color: #f9fafb;
  min-height: 100vh;
}

/* ==================== HEADER ==================== */
.settings-header {
  background-color: #f9fafb;
  padding: 28px 40px 20px 40px;
}

.settings-header h1 {
  font-size: 32px;
  font-weight: 700;
  color: #111827;
  margin-bottom: 6px;
  letter-spacing: -0.5px;
}
 
 .subtitle {
  color: #6b7280;
  font-size: 15px;
  font-weight: 400;
}

/* ==================== CONTENT LAYOUT ==================== */
.settings-content {
  display: flex;
  gap: 24px;
  padding: 0 40px 40px 40px;
}

/* ==================== SIDEBAR ==================== */
.settings-sidebar {
  width: 240px;
 background: white;
  border-radius: 12px;
  padding: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  border: 1px solid #e5e7eb;
  height: fit-content;
  position: sticky;
  top: 20px;
}

.settings-tab {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  background: transparent;
  border: none;
  border-radius: 8px;
  color: #6b7280;
font-size: 15px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  text-align: left;
}

.settings-tab:hover {
  background: #f3f4f6;
  color: #111827;
}

.settings-tab.active {
  background: #eff6ff;
  color: #2563eb;
  font-weight: 600;
}

.tab-icon {
  font-size: 18px;
}

/* ==================== MAIN CONTENT ==================== */
.settings-main {
  flex: 1;
}

.settings-section {
  background: white;
  border-radius: 12px;
  padding: 32px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  border: 1px solid #e5e7eb;
}

.section-title {
  font-size: 24px;
  font-weight: 700;
  color: #111827;
  margin-bottom: 24px;
}

/* ==================== PROFILE CARD ==================== */
.profile-card {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.profile-avatar-section {
  display: flex;
  align-items: center;
  gap: 24px;
  padding-bottom: 24px;
  border-bottom: 1px solid #e5e7eb;
}

.profile-avatar-large {
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, #14b8a6 0%, #0d9488 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 28px;
  font-weight: 700;
}

.helper-text {
  font-size: 12px;
  color: #9ca3af;
  margin-top: 8px;
}

/* ==================== FORMS ==================== */
.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group label {
  font-size: 14px;
  font-weight: 600;
  color: #374151;
}

.form-input,
.form-select {
  padding: 10px 14px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 15px;
  color: #111827;
  transition: all 0.2s ease;
}

.form-input:focus,
.form-select:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.form-input:disabled {
  background: #f3f4f6;
  color: #9ca3af;
  cursor: not-allowed;
}

.form-actions {
  display: flex;
  gap: 12px;
  padding-top: 8px;
}

/* ==================== BUTTONS ==================== */
.btn-primary {
  padding: 10px 20px;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-primary:hover {
  background: #2563eb;
}

.btn-secondary {
  padding: 10px 20px;
  background: transparent;
  color: #6b7280;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-secondary:hover {
  background: #f3f4f6;
  color: #111827;
}

.btn-danger {
  padding: 10px 20px;
  background: #ef4444;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-danger:hover {
  background: #dc2626;
}

/* ==================== SETTINGS CARD ==================== */
.settings-card {
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 24px;
}

.card-subtitle {
  font-size: 18px;
  font-weight: 600;
  color: #111827;
  margin-bottom: 20px;
}

.setting-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 0;
  border-bottom: 1px solid #e5e7eb;
}

.setting-item:last-child {
  border-bottom: none;
}

.setting-info h4 {
  font-size: 15px;
  font-weight: 600;
  color: #111827;
  margin-bottom: 4px;
}

.setting-info p {
  font-size: 13px;
  color: #6b7280;
}

/* ==================== TOGGLE SWITCH ==================== */
.toggle-switch {
  position: relative;
  display: inline-block;
  width: 50px;
  height: 28px;
}

.toggle-switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.toggle-slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #d1d5db;
  transition: 0.3s;
  border-radius: 28px;
}

.toggle-slider:before {
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

input:checked + .toggle-slider {
  background-color: #3b82f6;
}

input:checked + .toggle-slider:before {
  transform: translateX(22px);
}

/* ==================== DANGER ZONE ==================== */
.danger-zone {
  border: 2px solid #fecaca;
  background: #fef2f2;
}

.danger-zone p {
  color: #991b1b;
  margin-bottom: 16px;
}

/* ==================== ABOUT ==================== */
.about-item {
  display: flex;
  justify-content: space-between;
  padding: 12px 0;
  border-bottom: 1px solid #e5e7eb;
}

.about-item:last-child {
  border-bottom: none;
}

.about-label {
  font-size: 14px;
  color: #6b7280;
  font-weight: 500;
}

.about-value {
  font-size: 14px;
  color: #111827;
  font-weight: 600;
}

/* ==================== RESPONSIVE ==================== */
@media (max-width: 1024px) {
  .settings-content {
    flex-direction: column;
  }
  
  .settings-sidebar {
    width: 100%;
    position: static;
  }
}
</style>  
