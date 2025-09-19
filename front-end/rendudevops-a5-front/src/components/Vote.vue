<!-- <script setup>
import { ref } from 'vue'

const nom = ref('')
const prenom = ref('')
const mail = ref('')
const reponse = ref('')
const message = ref('')

async function submitForm() {
  const payload = {
    nom: nom.value,
    prenom: prenom.value,
    mail: mail.value,
    resultat_vote: reponse.value
  }

  try {
    const response = await fetch('http://localhost:7071/api/postVote', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
    })
    const result = await response.json()
    if (response.ok) {
      message.value = "Votre vote a bien été enregistré !"
      // Optionnel : reset le formulaire
      nom.value = ''
      prenom.value = ''
      mail.value = ''
      reponse.value = ''
    } else {
      message.value = result.error || "Erreur lors de l'enregistrement du vote."
    }
    console.log('Réponse API:', result)
  } catch (error) {
    message.value = "Erreur réseau ou serveur."
    console.error('Erreur POST:', error)
  }
}
</script> -->


<script setup>
import { ref } from 'vue'

const nom = ref('')
const prenom = ref('')
const mail = ref('')
const reponse = ref('')
const message = ref('')

// Fonction pour récupérer le tableau de votes depuis localStorage
function getStoredVotes() {
  const stored = localStorage.getItem('votes')
  return stored ? JSON.parse(stored) : []
}

// Fonction pour sauvegarder le tableau de votes dans localStorage
function saveVotesLocally(votes) {
  localStorage.setItem('votes', JSON.stringify(votes))
}

async function submitForm() {
  const payload = {
    nom: nom.value,
    prenom: prenom.value,
    mail: mail.value,
    resultat_vote: reponse.value
  }

  try {
    // POST vers ton API
    const response = await fetch('http://localhost:7071/api/postVote', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
    })
    const result = await response.json()

    if (response.ok) {
      message.value = "Votre vote a bien été enregistré !"

      // 1️⃣ Stocker localement
      const votes = getStoredVotes()
      votes.push(payload)  // Ajouter le nouveau vote
      saveVotesLocally(votes)

      // 2️⃣ Réinitialiser le formulaire
      nom.value = ''
      prenom.value = ''
      mail.value = ''
      reponse.value = ''
    } else {
      message.value = result.error || "Erreur lors de l'enregistrement du vote."
    }

    console.log('Réponse API:', result)
    console.log('Votes stockés localement:', getStoredVotes())
  } catch (error) {
    message.value = "Erreur réseau ou serveur."
    console.error('Erreur POST:', error)
  }
}
</script>

<template>
  <form class="vote-form" @submit.prevent="submitForm">
    <div class="form-group">
      <label for="nom">Nom :</label>
      <input type="text" id="nom" v-model="nom" required />
    </div>
    <div class="form-group">
      <label for="prenom">Prénom :</label>
      <input type="text" id="prenom" v-model="prenom" required />
    </div>
    <div class="form-group">
      <label for="mail">Email :</label>
      <input type="email" id="mail" v-model="mail" required />
    </div>
    <div class="form-group">
      <label>Votre réponse :</label>
      <div>
        <label>
          <input type="radio" value="oui" v-model="reponse" required />
          Oui
        </label>
        <label>
          <input type="radio" value="non" v-model="reponse" required />
          Non
        </label>
      </div>
    </div>
    <button type="submit">Voter</button>
    <p v-if="message" class="vote-message">{{ message }}</p>
  </form>
</template>

<style scoped>
.vote-form {
  max-width: 400px;
  margin: 0 auto;
  padding: 24px;
  background: #f9f9f9;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}
.form-group {
  margin-bottom: 16px;
}
label {
  display: block;
  margin-bottom: 6px;
  color: #444;
}
input[type="text"],
input[type="email"] {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 6px;
}
input[type="radio"] {
  margin-right: 6px;
}
button {
  padding: 10px 24px;
  background: #16a34a;
  color: #fff;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}
button:hover {
  background: #128039;
}
.vote-message {
  margin-top: 12px;
  color: #128039;
  font-size: 1rem;
}
</style>