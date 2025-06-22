<script setup>
import { useRouter } from "vue-router";

const router = useRouter();

const onSubmit = () => {
  router.push("/login");
}
</script>

<template>
<div class="wrapper">
  <h1>Anonymous Chat</h1>
  <br>
  <p>Chat does not save messages and history, you can <br>
    communicate freely without worrying about your privacy.</p>
  <br>
  <p>To start chatting, click on the button below</p>
  <el-button type="primary" @click="onSubmit" size="large" >Start!</el-button>

</div>
</template>

<style scoped>
  .wrapper {
    margin-left: 450px;
    margin-top: 150px;
    margin-right: 450px;
    border: 3px cornflowerblue solid;
    border-radius: 10px;
    padding: 15px;
  }
  p {
    font-size: 20px;
  }
  h1 {font-size: 50px;
    }

</style>