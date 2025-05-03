<script setup>
import Chat from './components/Chat.vue'
import Login from './components/Login.vue'


</script>

<template>
<!--  <div class="login_wrapper">-->
<!--    <Login class="login" ></Login>-->
<!--  </div>-->
  <Chat></Chat>
</template>

<style scoped>
  .login_wrapper {
    height: 650px;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .login {
    padding: 20px;
    border: 3px cornflowerblue solid;
    border-radius: 10px;

  }
</style>
