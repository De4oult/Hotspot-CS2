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
        <div class="flex flex-col w-full items-center mt-4 px-8 mb-8">
            <MapCard 
                v-for="map in maps" 
                :key="map.id" 
                class="mt-5" 
                :map="map" 
                @toggleSelected="toggleSelected" 
            />
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { io } from 'socket.io-client';
import MapCard from '../components/MapCard.vue';

const socket = io('http://localhost:8000');  // URL для подключения к серверу WebSocket на Node.js

const maps = ref([]);
const currentStage = ref('ban');
const currentTurn = ref(0);
const myTeamId = ref(null);

onMounted(() => {
  const urlParams = new URLSearchParams(window.location.search);
  myTeamId.value = parseInt(urlParams.get('teamId'), 10);

  socket.on('initialData', (data) => {
    console.log('Received initialData:', data);
    maps.value = data.maps;
    currentStage.value = data.currentStage;
    currentTurn.value = data.currentTurn;
  });

  socket.on('updateData', (data) => {
    console.log('Received updateData:', data);
    maps.value = data.maps;
    currentTurn.value = data.currentTurn;
  });
});

const isMyTurn = computed(() => currentTurn.value === myTeamId.value);

const toggleSelected = (mapId) => {
  const map = maps.value.find(m => m.id === mapId);
  if (isMyTurn.value) {
    if (currentStage.value === 'ban') {
      socket.emit('banMap', { mapId });
    } else if (currentStage.value === 'pick') {
      socket.emit('pickMap', { mapId });
    }
  }
};
</script>
<!-- 
<script setup>
    import { ref } from 'vue';
    import MapCard from '../components/MapCard.vue';
    import InfernoTitle from '../assets/maps/inferno_title.svg';
    import VertigoTitle from '../assets/maps/vertigo_title.svg';
    import NukeTitle from '../assets/maps/nuke_title.svg';
    import OverpassTitle from '../assets/maps/overpass_title.svg';
    import AssemblyTitle from '../assets/maps/assembly_title.svg';
    import MementoTitle from '../assets/maps/memento_title.svg';

    const maps = ref([
        { id: 1, title: InfernoTitle, previewUrl: 'https://ukocgukpmdoflluaaiob.supabase.co/storage/v1/object/public/maps/inferno.png' },
        { id: 2, title: VertigoTitle, previewUrl: 'https://ukocgukpmdoflluaaiob.supabase.co/storage/v1/object/public/maps/vertigo.png' },
        { id: 3, title: NukeTitle, previewUrl: 'https://ukocgukpmdoflluaaiob.supabase.co/storage/v1/object/public/maps/nuke.png' },
        { id: 4, title: OverpassTitle, previewUrl: 'https://ukocgukpmdoflluaaiob.supabase.co/storage/v1/object/public/maps/overpass.png' },
        { id: 5, title: AssemblyTitle, previewUrl: 'https://ukocgukpmdoflluaaiob.supabase.co/storage/v1/object/public/maps/assembly.png' },
        { id: 6, title: MementoTitle, previewUrl: 'https://ukocgukpmdoflluaaiob.supabase.co/storage/v1/object/public/maps/memento.png' }
    ]);
</script> -->
