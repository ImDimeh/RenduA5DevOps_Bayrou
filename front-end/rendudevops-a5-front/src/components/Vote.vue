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
  </form>
</template>

<script setup>
import { ref } from 'vue'

const nom = ref('')
const prenom = ref('')
const mail = ref('')
const reponse = ref('')

function submitForm() {
  // Traitement du formulaire (affichage console pour exemple)
  console.log({
    nom: nom.value,
    prenom: prenom.value,
    mail: mail.value,
    reponse: reponse.value
  })
  // Tu peux ajouter ici l'envoi vers une API ou autre action
}
</script>

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
</style>