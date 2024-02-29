<script setup>
import { defineProps } from 'vue';

const props = defineProps({
  me: Object,
  message: Object,
});

let image = './src/assets/chatbot.jpg';
</script>

<template>
  <li :key="message.id" :class="message.user_id === me.id ? 'messagesMessage currentMember' : 'messagesMessage'">
    <span class="avatar" :style="{ backgroundColor: message.user_id === me.id ? '#ccc' : '#999' }" />
    

    <div class="messageContent">
      <div class="username">{{ message?.username || '' }}</div>
      <div class="text"><pre style="white-space: break-spaces;">{{ message?.data }}</pre></div>
    </div>
  </li>
</template>