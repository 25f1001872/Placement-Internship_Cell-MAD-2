<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-5">
        <div class="card p-4">
          <h3 class="mb-3 text-center">Login</h3>
          <div v-if="error" class="alert alert-danger">{{ error }}</div>
          <div class="mb-3">
            <label class="form-label">Email</label>
            <input v-model="email" type="email" class="form-control" />
          </div>
          <div class="mb-3">
            <label class="form-label">Password</label>
            <input v-model="password" type="password" class="form-control" />
          </div>
          <button @click="login" class="btn btn-primary w-100">Login</button>
          <div class="mt-3 text-center">
            <router-link to="/register/student">Register as Student</router-link> |
            <router-link to="/register/company">Register as Company</router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../utils/api'

export default {
  data() {
    return { email: '', password: '', error: '' }
  },
  methods: {
    async login() {
      try {
        const res = await api.post('/api/auth/login', { email: this.email, password: this.password })
        localStorage.setItem('token', res.data.token)
        localStorage.setItem('role', res.data.role)
        localStorage.setItem('name', res.data.name)
        this.$router.push(`/${res.data.role}/dashboard`)
      } catch (err) {
        this.error = err.response?.data?.error || 'Login failed'
      }
    }
  }
}
</script>