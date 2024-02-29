<script setup>
import { ref, defineProps } from 'vue';


const props = defineProps({
  onSendMessage: Function,
  loading: Boolean,
});

const text = ref('');

function onSubmit() {
  props.onSendMessage(text.value);
  text.value = '';
}

</script>

<template>
  <div class="input">
    <form @submit.prevent="onSubmit">
      <input v-model="text" />
      <button type="button" :disabled="loading" @click="onSubmit">{{loading ? 'Wait...' : 'Send'}}</button>
    </form>
  </div>
</template>