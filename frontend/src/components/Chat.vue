<template>
  <div class="chat-wrapper">
    <el-page-header @back="onBack" >
      <template #content>
        <div class="flex items-center">
          <el-avatar
              :size="36"
              class="mr-3"

          > <el-icon :size="25" v-if="companionInfo.gender == 'Male'"><Male /></el-icon>
            <el-icon :size="25" v-else><Female /> </el-icon> </el-avatar>
          <span class="text-large font-600 mr-3"> {{ '&nbsp;&nbsp;' + companionInfo.nickname + '&nbsp;&nbsp;&nbsp;'}} </span>

          <span class="text-sm mr-2" style="color: var(--el-text-color-regular)">
          {{companionInfo.age}} y.
        </span>
        </div>
      </template>
    </el-page-header>
    <hr>
    <ul
        ref="chatListRef"
        class="chat-list"
    >
      <li
          v-for="(msg, index) in messages"
          :key="index"
          class="list-item"
          :class="msg.type"
      >
        {{ msg.message }}
      </li>
    </ul>
    <hr>
    <div class="message-input">

      <el-input
          v-model="textarea"
          type="textarea"
          :autosize="{ minRows: 1, maxRows: 3 }"
          class="input"
          placeholder="Enter your message"
          resize="none"
          maxlength="512"
          @keydown.enter.prevent="sendMessage"
      />
      <el-button
          type="primary"
          :icon="Message"
          circle
          size="large"
          class="send-btn"
          @click="sendMessage"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import {ref, computed, nextTick, onMounted, onBeforeUnmount} from 'vue'
import {Female, Male, Message} from '@element-plus/icons-vue'
import {useRoute, useRouter} from "vue-router";
import { useSessionStore } from '@/stores/session'



const session = useSessionStore()

const companionInfo = session.companionInfo

const textarea = ref('')
const chatListRef = ref<HTMLElement | null>(null)

const scrollToBottom = async () => {
  await nextTick()
  if (chatListRef.value) {
    chatListRef.value.scrollTo({
      top: chatListRef.value.scrollHeight,
      behavior: 'smooth',
    })
  }
}
const router = useRouter()
const route = useRoute()

const wsUrl = route.query.ws
const username = ref(wsUrl.split('/').pop())
const roomId = ref(wsUrl.split('/')[wsUrl.split('/').length - 2])

const messages = ref([])
let socket = null

onMounted(() => {


  if (!wsUrl) {
    console.error('WebSocket URL не передан')
    return
  }

  socket = new WebSocket(wsUrl)

  socket.onopen = () => {
    console.log('🔌 WebSocket открыт')
  }

  socket.onmessage = (event) => {
    const msg = JSON.parse(event.data)
    let message

    if (msg.data === "disconnect") {
      message = {
        message: "Your interlocutor has completed the chat. Press the \"Back\" button to return to the menu.",
        type: "service-message",
      }
    } else {
      message = {
        message: msg.data,
        type: msg.username === username.value ? 'message-sent' : 'message-received'
      }
    }

    messages.value.push(message)
    scrollToBottom()
    console.log(msg.user, username.value)
  }

  socket.onerror = (err) => {
    console.error('❌ Ошибка WebSocket:', err)
  }

  socket.onclose = () => {
    console.log('🔌 WebSocket закрыт')
  }
})

onBeforeUnmount(() => {
  socket?.close()
})

const sendMessage = () => {
  console.log('➡️ sendMessage called')
  console.log('socket:', socket)
  console.log('readyState:', socket?.readyState)

  if (socket && socket.readyState === 1 && textarea.value.trim()) {
    console.log('📤 отправка:', textarea.value)
    socket.send(textarea.value)
    textarea.value = ''
  } else {
    console.log('❌ Сокет не готов или сообщение пустое')
  }
}

const onBack = async () => {
  socket.send("disconnect")
  if (socket && socket.readyState === 1) {
    socket.close(1000, "User cancelled")
  }
  await fetch(`http://localhost:8000/login/close?room_id=${roomId.value}`, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
  })
  await router.push({name: 'Login'})
}
</script>

<style scoped>
.chat-wrapper {
  width: 40%;
  margin: 0 auto;
  padding: 10px;
}

.chat-list {
  height: 480px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  padding: 10px;
  scroll-behavior: smooth;
}

.list-item {
  display: inline-block;
  padding: 10px 15px;
  border-radius: 20px;
  font-size: 14px;
  line-height: 1.4;
  word-wrap: break-word;
  word-break: break-word;
  white-space: normal;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  max-width: 40%;
}

.message-sent {
  background-color: #dcf8c6;
  color: #333;
  align-self: flex-end;
  margin-left: auto;
  border-bottom-right-radius: 0;
}

.message-received {
  background-color: cornflowerblue;
  color: white;
  align-self: flex-start;
  margin-right: auto;
  border-bottom-left-radius: 0;
}

.message-input {
  display: flex;
  align-items: flex-start;
  margin-top: 15px;
}

.input {
  flex: 1;
  max-width: 90%;
}

.send-btn {
  margin-left: 15px;
}
hr {
  border: none;
  height: 1px;
  background: linear-gradient(to right, transparent, #ccc, transparent);
  margin: 20px 0;
}

.service-message {
  color: gray;
  font-style: italic;
  text-align: center;

}
</style>