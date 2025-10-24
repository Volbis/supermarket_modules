# 🛒 Module de Gestion des Caisses - ExpressMall

Module frontend de gestion des caisses pour supermarché, construit avec **Vue.js 3** et **Electron**.

## 📋 Description

Ce module permet de gérer l'ensemble du processus de caisse en supermarché, incluant:
- ✅ Point de vente (scan/saisie produits)
- ✅ Gestion des paiements multi-méthodes
- ✅ Promotions et remises
- ✅ Programme de fidélité
- ✅ Rapports quotidiens
- ✅ Clôture de caisse
- ✅ Historique des transactions

## 🛠️ Technologies utilisées

- **Vue.js 3** - Framework JavaScript progressif
- **Electron** - Pour créer l'application desktop
- **Axios** - Client HTTP pour les API
- **Chart.js** - Graphiques et visualisations
- **Tailwind CSS** - Framework CSS utilitaire

## 🚀 Installation

### Prérequis
- Node.js >= 14.x
- npm >= 6.x

### Étapes d'installation

1. **Installer les dépendances**
   ```bash
   npm install
   ```

2. **Configurer les variables d'environnement**
   Créer un fichier `.env` à la racine:
   ```env
   VUE_APP_API_URL=http://localhost:8000/api
   ```

3. **Lancer le serveur de développement**
   ```bash
   npm run serve
   ```
   L'application sera accessible sur `http://localhost:8082`

4. **Lancer l'application Electron (mode développement)**
   ```bash
   npm run electron:dev
   ```

## 📁 Structure du projet

```
front_caisses/
├── electron/               # Configuration Electron
├── public/                 # Fichiers publics statiques
├── src/
│   ├── api/               # Configuration Axios
│   ├── assets/            # Assets (CSS, images, icônes)
│   ├── composables/       # Composables Vue (logique réutilisable)
│   ├── services/          # Services API
│   ├── views/             # Vues/Pages de l'application
│   ├── App.vue            # Composant racine
│   └── main.js            # Point d'entrée
├── package.json
├── tailwind.config.js
└── vue.config.js
```

## 🎨 Design System

Le module respecte strictement le design system du module de gestion de stocks avec des couleurs soft et épurées.

## 📦 Build Production

```bash
npm run build
```

## 👥 Équipe de développement

- **Projet**: ExpressMall - Gestion des Caisses
- **Version**: 1.0.0

---

**ExpressMall** - Votre solution complète de gestion de supermarché 🛒✨
