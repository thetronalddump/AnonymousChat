<template>
  <div class="login-wrapper">
  <div class="login">

  <el-form :model="form" label-width="auto" style="max-width: 400px" v-loading="disableFlag">
    <h1>Login</h1>
    <el-form-item label="Nickname" >
      <el-input v-model="form.nickname" :disabled="disableFlag"/>
    </el-form-item>
    <el-form-item label="Age">
      <el-col :span="11">
        <el-input-number
            v-model="form.age"
            style="width: 150px"
            min=16
            value-on-clear=18
            :disabled="disableFlag"

        />
      </el-col>
    </el-form-item>
    <el-form-item label="Gender">
      <el-radio-group v-model="form.gender" :disabled="disableFlag">
        <el-radio value="Male">Male</el-radio>
        <el-radio value="Female">Female</el-radio>
      </el-radio-group>
    </el-form-item>
  </el-form>
    <el-button :type="buttonType" @click="onSubmit" style="">{{ buttonText }}</el-button>
  </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const buttonType = ref('primary')
const buttonText = ref('Search!')
const disableFlag = ref(false)
const form = reactive({
  nickname: '',
  age: '',
  gender: ''
})

const onSubmit = async () => {
  if (buttonType.value === 'primary') {
    buttonType.value = 'danger'
    buttonText.value = 'Cancel'
    disableFlag.value = true
    try {
      const res = await fetch('http://localhost:8000/login/search', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(form)
      })

      const data = await res.json()
      const wsUrl = data.url
      await router.push({name: 'Chat', query: {ws: wsUrl}})

    } catch (err) {
      console.error('Ошибка при логине:', err)
    }
  } else {
    buttonType.value = 'primary'
    buttonText.value = 'Search!'
    disableFlag.value = false
    await fetch('http://localhost:8000/login/close', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(form)
    })
  }

}

</script>

<style scoped>
  h1 {
    text-align: center;
  }
  .login-wrapper {
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