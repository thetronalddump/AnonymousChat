<template>
  <div>

  <el-form :model="form" label-width="auto" style="max-width: 400px">
    <h1>Login</h1>
    <el-form-item label="Nickname">
      <el-input v-model="form.name" />
    </el-form-item>
    <el-form-item label="Date of birth">
      <el-col :span="11">
        <el-date-picker
            v-model="form.date_of_birth"
            type="date"
            placeholder="Pick a date"
            style="width: 150px"
        />
      </el-col>
    </el-form-item>
    <el-form-item label="Gender">
      <el-radio-group v-model="form.gender">
        <el-radio value="Male">Male</el-radio>
        <el-radio value="Female">Female</el-radio>
      </el-radio-group>
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="onSubmit" style="">Create</el-button>
    </el-form-item>
  </el-form>
  </div>
</template>

<script setup>
import { reactive } from 'vue'


const form = reactive({
  name: '',
  date_of_birth: '',
  gender: ''
})

const onSubmit = () => {
  console.log('submit!')
}
</script>

<style scoped>
  h1 {
    text-align: center;
  }

</style>