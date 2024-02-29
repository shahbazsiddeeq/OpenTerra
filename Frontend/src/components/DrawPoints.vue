<template>
  <div>
    <!-- <div style="position:absolute; width:30%;">{{ vectors }}</div> -->
    <button
      v-if="vectors.length > 0"
      type="button"
      @click="resetVector()"
      style="position: absolute; left: 30%"
    >
      Reset
    </button>
    <div
      ref="container"
      style="position: absolute; right: 0; width: 64%; height: 100%"
    ></div>
    <div class="appContent">
      <div class="chat-header"><img src="../assets/chatbot.jpg" class="avatar" /> <span style="vertical-align: super;">Climagrün AI Assistant</span></div>
      <Messages :messages="messages" :me="me" />
      <Input :loading="loading" :onSendMessage="onSendMessage" />
    </div>
  </div>
</template>

<script>
import * as THREE from "three";
import axios from "axios";
import Messages from "../components/Messages.vue";
import Input from "../components/Input.vue";

export default {
  name: "DrawPoints",
  components: {
    Messages,
    Input,
  },
  data() {
    return {
      loading: false,
      vectors: [],
      adjectives: ["Autumn", "Hidden", "Bitter", "Nameless"],
      nouns: ["Waterfall", "River", "Breeze", "Moon", "Rain"],
      messages: [],
      me: {
        id: Math.random(),
        username: null,
        color: null,
      },
    };
  },
  mounted() {
    this.initThree();
    this.me.username = this.randomName();
    this.me.color = this.randomColor();
    let messages = localStorage.getItem("messages");
    if (messages) {
      this.messages = JSON.parse(messages);
    }
    let me = localStorage.getItem("me");
    if (me) {
      this.me = JSON.parse(me);
    }
  },
  methods: {
    resetVector() {
      this.vectors = [];
      this.clearCanvas();
      this.initThree();
    },
    clearCanvas() {
      const container = this.$refs.container;
      container.innerHTML = "";
    },
    randomColor() {
      return "#" + Math.floor(Math.random() * 0xffffff).toString(16);
    },
    randomName() {
      const adjective =
        this.adjectives[Math.floor(Math.random() * this.adjectives.length)];
      const noun = this.nouns[Math.floor(Math.random() * this.nouns.length)];
      return adjective+ " " + noun;
      // return "ClimaGrün AI Assistant";
    },
    onSendMessage(message) {
      this.loading = true;
      let form = {
        chatId: "202",
        prompt: message,
        vertices: this.vectors,
      };
      localStorage.setItem("me", JSON.stringify(this.me));
      this.pushMessages(message);
      axios
        .post("http://127.0.0.1:8000/completion/", form)
        .then((response) => {
          if (response?.status === 200) {
            this.pushServerResponse(response);
          }
        })
        .catch((error) => {
          console.log(error);
        })
        .finally(() => {
          this.loading = false;
        });
    },
    pushMessages(message) {
      this.messages.push({
        id: Math.random(),
        user_id: this.me?.id,
        username: this.me?.username,
        data: message,
      });
    },
    pushServerResponse(response) {
      this.messages.push({
        id: Math.random(),
        user_id: Math.random(),
        username: this.randomName(),
        data: response?.data?.choices?.[0]?.message?.content,
      });
      localStorage.setItem("messages", JSON.stringify(this.messages));
    },
    initThree() {
      const container = this.$refs.container;
      const width = container.offsetWidth;
      const height = window.innerHeight;

      const scene = new THREE.Scene();
      scene.background = new THREE.Color("gainsboro");
      

      const camera = new THREE.OrthographicCamera(
        -width / 2,
        width / 2,
        height / 2,
        -height / 2,
        -10,
        10
      );
      camera.position.set(0, 0, 10);
      camera.lookAt(scene.position);

      const renderer = new THREE.WebGLRenderer({ antialias: true });
      renderer.setSize(width, height);
      container.appendChild(renderer.domElement);

      const points = [];
      const polygon = new THREE.Mesh(
        new THREE.BufferGeometry(),
        new THREE.MeshBasicMaterial({
          color: "crimson",
          transparent: true,
          opacity: 0.4,
          side: THREE.DoubleSide,
          depthTest: false,
        })
      );

      scene.add(polygon);
      renderer.render(scene, camera);

      container.addEventListener("click", (event) => {
        const rect = container.getBoundingClientRect();
        const x = event.clientX - rect.left - width / 2;
        const y = height / 2 - (event.clientY - rect.top);

        const point = new THREE.Mesh(
          new THREE.CircleGeometry(5),
          new THREE.MeshBasicMaterial({ color: "#000" })
        );
        point.position.set(x, y, 0);
        scene.add(point);

        points.push(new THREE.Vector2(x, y));
        if (points.length > 1) {
          const shape = new THREE.Shape(points);
          polygon.geometry.dispose();
          polygon.geometry = new THREE.ShapeGeometry(shape);
        }

        this.vectors.push({ x: x, y: y });
        renderer.render(scene, camera);
      });
    },
  },
};
</script>

<style scoped>
body {
  overflow: hidden;
  margin: 0;
  height: 100vh;
  width: 100vw;
}
</style>
