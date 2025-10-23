<template>
  <div class="login-container">
    <div class="login-card">
      <!-- Logo et titre -->
      <div class="login-header">
        <div class="logo">
          <div class="logo-icon">EM</div>
          <h1>ExpressMall</h1>
        </div>
        <p class="subtitle">Connectez-vous à votre compte</p>
      </div>

      <!-- Formulaire de connexion -->
      <form @submit.prevent="handleLogin" class="login-form">
        <!-- Message d'erreur -->
        <div v-if="error" class="error-message">
          <span class="error-icon">⚠️</span>
          <p>{{ error }}</p>
        </div>

        <!-- Champ username -->
        <div class="form-group">
          <label for="username">Nom d'utilisateur</label>
          <input
            id="username"
            v-model="credentials.username"
            type="text"
            class="form-input"
            placeholder="Entrez votre nom d'utilisateur"
            required
            :disabled="loading"
          />
        </div>

        <!-- Champ password -->
        <div class="form-group">
          <label for="password">Mot de passe</label>
          <input
            id="password"
            v-model="credentials.password"
            type="password"
            class="form-input"
            placeholder="Entrez votre mot de passe"
            required
            :disabled="loading"
          />
        </div>

        <!-- Se souvenir de moi -->
        <div class="form-options">
          <label class="checkbox-label">
            <input type="checkbox" v-model="rememberMe" />
            <span>Se souvenir de moi</span>
          </label>
        </div>

        <!-- Bouton de connexion -->
        <button type="submit" class="login-btn" :disabled="loading">
          <span v-if="!loading">Se connecter</span>
          <span v-else>
            <span class="spinner-small"></span>
            Connexion en cours...
          </span>
        </button>
      </form>

      <!-- Informations supplémentaires -->
      <div class="login-footer">
        <p class="info-text">Comptes de démonstration disponibles :</p>
        <div class="demo-accounts">
          <div class="demo-account">
            <strong>Admin:</strong> admin / admin123
          </div>
          <div class="demo-account">
            <strong>Manager:</strong> manager1 / manager123
          </div>
          <div class="demo-account">
            <strong>Vendeur:</strong> vendeur1 / vendeur123
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import authService from '@/services/auth';

export default {
  name: 'LoginView',
  data() {
    return {
      credentials: {
        username: '',
        password: ''
      },
      rememberMe: false,
      loading: false,
      error: null
    };
  },
  methods: {
    async handleLogin() {
      this.error = null;
      this.loading = true;

      try {
        const response = await authService.login(
          this.credentials.username,
          this.credentials.password
        );

        console.log('Connexion réussie:', response);
        
        // Rediriger vers la page d'accueil ou dashboard
        this.$emit('login-success', response.user);
        
        // Si vous utilisez Vue Router, décommentez cette ligne
        // this.$router.push({ name: 'Dashboard' });
        
      } catch (error) {
        console.error('Erreur de connexion:', error);
        
        if (error.response) {
          // Erreur de réponse du serveur
          if (error.response.status === 400) {
            this.error = 'Identifiants invalides. Veuillez réessayer.';
          } else if (error.response.status === 500) {
            this.error = 'Erreur serveur. Veuillez réessayer plus tard.';
          } else {
            this.error = error.response.data.message || 'Une erreur est survenue.';
          }
        } else if (error.request) {
          // Pas de réponse du serveur
          this.error = 'Impossible de contacter le serveur. Vérifiez votre connexion.';
        } else {
          // Autre erreur
          this.error = 'Une erreur est survenue. Veuillez réessayer.';
        }
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.login-card {
  background: white;
  border-radius: 20px;
  padding: 40px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  max-width: 450px;
  width: 100%;
  animation: slideUp 0.5s ease-out;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.login-header {
  text-align: center;
  margin-bottom: 32px;
}

.logo {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  margin-bottom: 8px;
}

.logo-icon {
  width: 70px;
  height: 70px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 28px;
  font-weight: 700;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.login-header h1 {
  font-size: 28px;
  font-weight: 700;
  color: #1e293b;
  margin: 0;
}

.subtitle {
  font-size: 15px;
  color: #64748b;
  margin: 0;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.error-message {
  background: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 10px;
  padding: 12px 16px;
  display: flex;
  align-items: center;
  gap: 12px;
}

.error-icon {
  font-size: 20px;
}

.error-message p {
  color: #dc2626;
  font-size: 14px;
  margin: 0;
  font-weight: 500;
}

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

.form-input {
  padding: 12px 16px;
  border: 2px solid #e5e7eb;
  border-radius: 10px;
  font-size: 15px;
  color: #1e293b;
  transition: all 0.2s ease;
}

.form-input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-input:disabled {
  background: #f3f4f6;
  cursor: not-allowed;
}

.form-options {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #475569;
  cursor: pointer;
}

.checkbox-label input[type="checkbox"] {
  width: 18px;
  height: 18px;
  cursor: pointer;
}

.login-btn {
  padding: 14px 24px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.login-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
}

.login-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none;
}

.spinner-small {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  display: inline-block;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.login-footer {
  margin-top: 32px;
  padding-top: 24px;
  border-top: 1px solid #e5e7eb;
}

.info-text {
  font-size: 13px;
  color: #64748b;
  text-align: center;
  margin-bottom: 12px;
  font-weight: 600;
}

.demo-accounts {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.demo-account {
  background: #f8fafc;
  padding: 10px 14px;
  border-radius: 8px;
  font-size: 13px;
  color: #475569;
  text-align: center;
}

.demo-account strong {
  color: #1e293b;
  margin-right: 8px;
}

@media (max-width: 480px) {
  .login-card {
    padding: 30px 24px;
  }

  .login-header h1 {
    font-size: 24px;
  }

  .logo-icon {
    width: 60px;
    height: 60px;
    font-size: 24px;
  }
}
</style>
