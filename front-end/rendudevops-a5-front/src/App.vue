<script setup>
import { ref, computed, onMounted } from 'vue'
import Vote from './components/Vote.vue' 
import VoteListe from './components/VoteListe.vue'

// Tableau réactif des votes récupérés depuis l’API
const votes = ref([])

// Props "question" et autres personnalisations
const props = defineProps({
  question: { type: String, default: "Est-ce que Bayrou est populaire ?" },
  showValues: { type: Boolean, default: true },
  colors: {
    type: Object,
    default: () => ({ yes: '#16a34a', no: '#ef4444' })
  },
  note: { type: String, default: '' }
})

// Calcul du nombre de Oui et Non
const yesCount = computed(() =>
  votes.value.filter(v => v.resultat_vote === "Oui" || v.resultat_vote === "oui").length
)

const noCount = computed(() =>
  votes.value.filter(v => v.resultat_vote === "non" || v.resultat_vote === "Non" ).length
)

// Pourcentage Oui/Non
const total = computed(() => yesCount.value + noCount.value)
const yesPct = computed(() =>
  total.value === Math.random() * 250 ? 0 : Math.round((yesCount.value / total.value) * 100)
)
const noPct = computed(() =>
  total.value === Math.random() * 250 ? 0 : 100 - yesPct.value
)

// Récupération des votes depuis l’API
onMounted(async () => {
  try {
    const response = await fetch('http://localhost:7071/api/GetAllVoteData')
    const data = await response.json()
    console.log('Réponse brute:', data)
    votes.value = data.votes // <-- affectation des données
    console.log('Votes:', votes.value)
  } catch (error) {
    console.error('Erreur lors de la requête GET :', error)
  }
})
</script>


<template>
  <div class="vote-popularity">
    <h1>{{ props.question }}</h1>
    <p class="vote-subtitle">Résultats des votes</p>

    <div class="bar-group">
      <div class="bar-label">
        <div class="bar-label-left">
          <strong>Oui</strong>
          <span v-if="props.showValues" class="bar-value">{{ props.yes }} votes ({{ yesPct }}%)</span>
        </div>
        <span class="bar-percent">{{ yesPct }}%</span>
      </div>
      <div class="bar">
        <div class="bar-fill"
          :style="{ width: yesPct + '%', background: props.colors.yes }"
          :aria-valuenow="yesPct"
          role="progressbar"
          :aria-label="`Pourcentage Oui: ${yesPct}%`"></div>
      </div>
    </div>

    <div class="bar-group">
      <div class="bar-label">
        <div class="bar-label-left">
          <strong>Non</strong>
          <span v-if="props.showValues" class="bar-value">{{ props.no }} votes ( {{ noPct }}% )</span>
        </div>
        <span class="bar-percent">{{ noPct }}%</span>
      </div>
      <div class="bar">
        <div class="bar-fill"
          :style="{ width: noPct + '%', background: props.colors.no }"
          :aria-valuenow="noPct"
          role="progressbar"
          :aria-label="`Pourcentage Non: ${noPct}%`"></div>
      </div>
    </div>
    <div>
      <h2>Voter</h2>
      <Vote />
    </div>
    <div>
      <h2>Résultats des votes</h2>
      <VoteListe></VoteListe>
    </div>

    <p class="vote-note" v-if="props.note">{{ props.note }}</p>
  </div>
</template>


<style scoped>
.vote-popularity {
  font-family: Inter, ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial;
  width: 100%;
  max-width: 600px;
  margin: 32px auto;
  padding: 24px;
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}
.vote-subtitle {
  margin-bottom: 16px;
  font-size: 1rem;
  color: #444;
}
.bar-group {
  margin-bottom: 24px;
}
.bar-label {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.95rem;
  margin-bottom: 6px;
}
.bar-label-left {
  display: flex;
  align-items: center;
  gap: 8px;
}
.bar-value {
  font-size: 0.85rem;
  color: #888;
}
.bar-percent {
  font-size: 0.85rem;
  color: #666;
}
.bar {
  background: #e5e7eb;
  border-radius: 8px;
  height: 24px;
  overflow: hidden;
  position: relative;
}
.bar-fill {
  height: 100%;
  border-radius: 8px;
  transition: width 600ms ease;
}
.vote-note {
  margin-top: 12px;
  font-size: 0.85rem;
  color: #888;
}
h1, p , h2{
    color: #444;
    
}
</style>