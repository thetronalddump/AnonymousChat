import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useSessionStore = defineStore('session', () => {
    const companionInfo = ref(null)

    function setCompanionInfo(info) {
        companionInfo.value = info
    }

    const wsUrl = ref(null)
    function setWebSocketUrl(url) {
        wsUrl.value = { ws: url }
    }

    return { companionInfo, setCompanionInfo, wsUrl, setWebSocketUrl }
})