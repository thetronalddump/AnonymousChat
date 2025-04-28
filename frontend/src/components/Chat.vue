<template>
  <div class="chat-wrapper">
    <ul
        ref="chatListRef"
        class="chat-list"
        v-infinite-scroll="load"
        :infinite-scroll-disabled="disabled"
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
          placeholder="Введите сообщение"
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
import { ref, computed, nextTick } from 'vue'
import { Message } from '@element-plus/icons-vue'

const textarea = ref('')
const messages = ref<{ message: string; type: string }[]>([])

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

const sendMessage = () => {
  if (!textarea.value.trim()) return

  messages.value.push({ message: textarea.value, type: 'message-sent' })
  messages.value.push({ message: textarea.value, type: 'message-received' })
  textarea.value = ''
  scrollToBottom()
}
</script>

<style scoped>
.chat-wrapper {
  width: 40%;
  margin: 0 auto;
  padding: 10px;
}

.chat-list {
  height: 500px;
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

</style>