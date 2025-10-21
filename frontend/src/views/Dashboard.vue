<template>
  <div class="dashboard-content">
    <div class="cards-grid-top">
      <div v-for="i in 3" :key="'top-' + i" class="dashboard-card card-top">
        Carte {{ i }}
      </div>
    </div>
    
    <div class="cards-grid-bottom">
      <div v-for="i in 2" :key="'bottom-' + i" class="dashboard-card card-bottom">
        Carte {{ i + 3 }}
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DashboardView'
}
</script>

<style scoped>
.dashboard-content {
  padding: 20px;
}

.cards-grid-top {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin-bottom: 20px;
}

.cards-grid-bottom {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

.dashboard-card {
  background: #F9F9FA;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  border: 1px solid #e5e7eb;
}

.card-top {
  min-height: 120px;
}

.card-bottom {
  min-height: 150px;
}
</style>