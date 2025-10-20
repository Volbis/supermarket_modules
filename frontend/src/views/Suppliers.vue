<template>
  <div class="suppliers-content">
    <div class="suppliers-header">
      <h2>Gestion des fournisseurs</h2>
      <p>Gérez vos partenaires fournisseurs</p>
      <button class="add-supplier-btn">+ Ajouter un fournisseur</button>
    </div>
    
    <div class="suppliers-list">
      <div v-for="supplier in suppliers" :key="supplier.id" class="supplier-card">
        <div class="supplier-info">
          <div class="supplier-avatar">
            {{ supplier.name.charAt(0) }}
          </div>
          <div class="supplier-details">
            <h3>{{ supplier.name }}</h3>
            <p>{{ supplier.email }}</p>
            <p>{{ supplier.phone }}</p>
            <span :class="['status-badge', supplier.status]">
              {{ supplier.status === 'active' ? 'Actif' : 'Inactif' }}
            </span>
          </div>
        </div>
        <div class="supplier-actions">
          <button class="action-btn edit">Modifier</button>
          <button class="action-btn contact">Contacter</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'FournisseursView',
  data() {
    return {
      suppliers: [
        {
          id: 1,
          name: 'Ferme Bio Martin',
          email: 'contact@fermebiomartin.fr',
          phone: '01 23 45 67 89',
          status: 'active'
        },
        {
          id: 2,
          name: 'Légumes du Sud',
          email: 'info@legumesdusud.com',
          phone: '04 56 78 90 12',
          status: 'active'
        },
        {
          id: 3,
          name: 'Fruits & Co',
          email: 'hello@fruitsco.fr',
          phone: '02 34 56 78 90',
          status: 'inactive'
        }
      ]
    }
  }
}
</script>

<style scoped>
.suppliers-content {
  padding: 20px;
}

.suppliers-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.suppliers-header h2 {
  font-size: 24px;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 8px;
}

.suppliers-header p {
  color: #6b7280;
  font-size: 16px;
}

.add-supplier-btn {
  padding: 12px 24px;
  background: #10b981;
  color: white;
  border: none;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
}

.add-supplier-btn:hover {
  background: #059669;
}

.suppliers-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 20px;
}

.supplier-card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  border: 1px solid #e5e7eb;
  padding: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.supplier-info {
  display: flex;
  align-items: center;
  gap: 16px;
}

.supplier-avatar {
  width: 50px;
  height: 50px;
  background: #3b82f6;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 18px;
}

.supplier-details h3 {
  font-size: 18px;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 4px;
}

.supplier-details p {
  color: #6b7280;
  font-size: 14px;
  margin-bottom: 4px;
}

.status-badge {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
}

.status-badge.active {
  background: #d1fae5;
  color: #065f46;
}

.status-badge.inactive {
  background: #fee2e2;
  color: #991b1b;
}

.supplier-actions {
  display: flex;
  gap: 8px;
}

.action-btn {
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
  font-size: 12px;
  cursor: pointer;
}

.action-btn.edit {
  background: #3b82f6;
  color: white;
}

.action-btn.contact {
  background: #10b981;
  color: white;
}

.action-btn:hover {
  opacity: 0.8;
}
</style>