<template>
  <div class="infinite-list-wrapper" style="overflow: auto">
    <ul
        v-infinite-scroll="load"
        class="list"
        :infinite-scroll-disabled="disabled"
    >
      <li v-for="i in messages" :key="i" class="list-item" :class="i.type">{{ i.message }}</li>
    </ul>
  </div>
  <div class="sending_message">
    <el-input
        v-model="textarea1"
        class="message_input"
        autosize
        type="textarea"
        placeholder="Input message"
        style="width: 35%"
        resize="none"
        maxlength="512">
    </el-input>
    <el-button type="primary" :icon="Message" circle class="sending_button" size="large" @click="send_message"/>
  </div>

  />
</template>

<script lang="ts" setup>
import { computed, ref } from 'vue'
import { Message } from '@element-plus/icons-vue'


const textarea1 = ref('')

const count = ref(1)
const messages = ref([])
const loading = ref(false)
const noMore = computed(() => count.value >= 20)
const disabled = computed(() => loading.value || noMore.value)
const load = () => {
  loading.value = true
  setTimeout(() => {
    count.value += 2
    loading.value = false
  }, 2000)
}

const send_message = () => {
  messages.value.push({
    "message": textarea1.value,
    "type": "message-sent"
  })
  messages.value.push({
    "message": textarea1.value,
    "type": "message-received"
  })
  textarea1.value = ''

}
</script>

<style>
.infinite-list-wrapper {
  height: 500px;
  text-align: center;

}
.infinite-list-wrapper .list {
  padding: 0;
  margin-right: 30%;
  margin-left: 30%;
  list-style: none;
  display: flex;
  flex-direction: column;
}


.list-item {
  white-space: normal;
  display: inline-block;
  max-width: 60%;
  padding: 10px 15px;
  border-radius: 20px;
  margin: 8px 0;
  font-size: 14px;
  line-height: 1.4;
  word-wrap: break-word;
  position: relative;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}
.infinite-list-wrapper .list-item + .list-item {
  margin-top: 10px;
}
.message_input {
  margin-left: 30%;
  margin-top: 25px;
}
.sending_button {
  margin-left: 20px;

}
.message-sent {
  background-color: #DCF8C6;
  align-self: flex-end;
  border-bottom-right-radius: 0;
  margin-left: auto;
  color: cornflowerblue;
}

.message-received {
  color: white;
  background-color: cornflowerblue;
  align-self: flex-start;
  border-bottom-left-radius: 0;
  margin-right: auto;
}
</style>