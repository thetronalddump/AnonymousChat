import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useSessionStore = defineStore('session', () => {
    const companionInfo = ref(null)

    function setCompanionInfo(info) {
        companionInfo.value = info
    }

    return { companionInfo, setCompanionInfo }
})