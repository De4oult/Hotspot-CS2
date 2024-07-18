<template>
        <div 
            class="relative flex items-center w-full h-28 bg-cover" 
            :style="{ backgroundImage: `url(${map.previewUrl})` }" 
            @click.prevent="toggleSelected"
        >
            <div class="absolute inset-0 bg-black opacity-25 transition-opacity duration-300"></div>
            <div class="flex items-center w-full h-full relative overflow-hidden">
                <div 
                    v-if="map.banned" 
                    class="flex flex-col w-32 h-full bg-red-500 z-10 justify-center transition-transform duration-300"
                    :class="translateClass"
                >
                <img :src="Ban" class="m-auto" />
                <h1 class="font-koulen text-white m-auto text-sm">BAN</h1>
            </div>
            <div 
                v-else-if="map.picked" 
                class="flex flex-col w-32 h-full bg-green-500 z-10 justify-center transition-transform duration-300"
                :class="translateClass"
            >
                <img :src="Pick" class="m-auto" />
                <h1 class="font-koulen text-white m-auto text-sm">PICK</h1>
            </div>
            <div class="flex justify-center w-full">
                <img 
                    :src="getImage(map.title)" 
                    class="z-10 transform transition-transform duration-300" 
                    :class="{ 'translate-x-16': selected }"
                >
            </div>
        </div>
    </div>
</template>
  
  <script setup>
    import { ref, computed } from 'vue';
    import Ban from '../assets/maps/ban.svg';
    import Pick from '../assets/maps/pick.svg';
    
    const props = defineProps({
        map: Object,
    });
    
    const emit = defineEmits(['toggleSelected']);
    
    const selected = ref(false);
    
    const toggleSelected = () => {
        selected.value = !selected.value;
        emit('toggleSelected', props.map.id);
    };

    const getImage = (title) => new URL(`../assets/maps/${title}_title.svg`, import.meta.url);
    
    const translateClass = computed(() => selected.value ? 'translate-x-0' : '-translate-x-full');
  </script>
  
  <style scoped>
  .transition-transform {
    transition-property: transform;
  }
  .translate-x-0 {
    transform: translateX(0);
  }
  .-translate-x-full {
    transform: translateX(-100%);
  }
  </style>
  