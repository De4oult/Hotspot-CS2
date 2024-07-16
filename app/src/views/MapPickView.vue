<!-- MapPickView.vue -->
<template>
    <div class="flex flex-col justify-center items-center">
      <div class="text-center">
        <h1 class="text-white text-4xl font-koulen tracking-[.3rem] p-3">00:30</h1>
      </div>
      <div class="text-center">
        <h1 class="font-koulen text-2xl tracking-[.3rem] bg-gradient-to-r from-yellow-500 via-red-500 to-red-600 bg-clip-text text-transparent">
          TEAM DE4OULT <span class="text-[#9AFF77]">PICK</span>
        </h1>
      </div>
      <div class="flex flex-col items-center mt-4 mx-7 mb-8">
        <MapCard 
          v-for="map in maps" 
          :key="map.id" 
          :map="map" 
          :currentTurn="currentTurn" 
          :isMyTurn="isMyTurn" 
          :currentStage="currentStage"
          @banMap="banMap" 
          @pickMap="pickMap" 
        />
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted, computed } from 'vue';
  import { io } from 'socket.io-client';
  import MapCard from '../components/MapCard.vue';
  
  const socket = io('http://localhost:8000');  // обновленный URL для подключения к серверу WebSocket на Python
  
  const maps = ref([]);
  const currentStage = ref('ban');
  const currentTurn = ref(0);
  const myTeamId = ref(parseInt(new URLSearchParams(window.location.search).get('teamId'), 10));
  
  const isMyTurn = computed(() => currentTurn.value === myTeamId.value);
  
  socket.on('initialData', (data) => {
    maps.value = data.maps;
    currentStage.value = data.currentStage;
    currentTurn.value = data.currentTurn;
  });
  
  socket.on('updateData', (data) => {
    maps.value = data.maps;
    currentTurn.value = data.currentTurn;
  });
  
  const banMap = (mapId) => {
    if (isMyTurn.value && currentStage.value === 'ban') {
      socket.emit('banMap', { mapId });
    }
  };
  
  const pickMap = (mapId) => {
    if (isMyTurn.value && currentStage.value === 'pick') {
      socket.emit('pickMap', { mapId });
    }
  };
  </script>
  