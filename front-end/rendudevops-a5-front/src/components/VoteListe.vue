<!-- <template>
    <div>
        <h2>Liste des votes</h2>
        <ul>
    <li v-for="vote in votes" :key="vote.id">
        {{ vote.nom }} - {{vote.prenom}} - {{ vote.resultat_vote }}
    </li>
    <p>{{ votes.value}}</p>
</ul>
    </div>
</template>

<script>
import { ref, onMounted } from 'vue'

export default {
    name: 'VoteListe',
    setup() {
        const votes = ref([])

       onMounted(async () => {
    try {
        const response = await fetch('http://localhost:7071/api/GetAllVoteData')
        const data = await response.json()
        
        votes.value = data.votes
        
    } catch (error) {
        console.error('Erreur lors de la requête GET :', error)
    }
})
        return { votes }
    }
}
</script> -->


<template>
  <div>
    <h2>Liste des votes</h2>
    <ul>
      <li v-for="vote in votes" :key="vote.id">
        {{ vote.nom }} - {{ vote.prenom }} - {{ vote.resultat_vote }}
      </li>
    </ul>
    <p>{{ votes }}</p>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'

export default {
  name: 'VoteListe',
  setup() {
    const votes = ref([])

    onMounted(() => {
      try {
        // Récupérer les votes depuis le localStorage
        const storedVotes = localStorage.getItem('votes') // clé 'votes'
        if (storedVotes) {
          votes.value = JSON.parse(storedVotes)
        } else {
          votes.value = [] // aucun vote stocké
        }
      } catch (error) {
        console.error('Erreur lors de la récupération des votes depuis localStorage :', error)
      }
    })

    return { votes }
  }
}
</script>
