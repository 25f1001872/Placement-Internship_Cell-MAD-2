<template>
  <div>
    <nav class="navbar border-bottom">
      <div class="container">
        <img src="/logo.svg" height="46" alt="Placement Portal" />
        <router-link to="/" class="btn btn-outline-dark btn-sm">Home</router-link>
      </div>
    </nav>

  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="card p-4">
          <h3 class="mb-3 text-center">Student Registration</h3>
          <div v-if="error" class="alert alert-danger">{{ error }}</div>
          <div v-if="message" class="alert alert-success">{{ message }}</div>
          <div class="mb-3">
            <label class="form-label">Name</label>
            <input v-model="form.name" type="text" class="form-control" />
          </div>
          <div class="mb-3">
            <label class="form-label">Email</label>
            <input v-model="form.email" type="email" class="form-control" />
          </div>
          <div class="mb-3">
            <label class="form-label">Password</label>
            <input v-model="form.password" type="password" class="form-control" />
          </div>
          <div class="mb-3">
            <label class="form-label">Education</label>
            <input v-model="form.education" type="text" class="form-control" />
          </div>
          <div class="mb-3">
            <label class="form-label">Skills</label>
            <input v-model="form.skills" type="text" class="form-control" />
          </div>
          <div class="mb-3">
            <label class="form-label">Experience</label>
            <input v-model="form.experience" type="text" class="form-control" />
          </div>
          <div class="mb-3">
            <label class="form-label">Contact</label>
            <input v-model="form.contact" type="text" class="form-control" />
          </div>
          <button @click="register" class="btn btn-dark w-100">Register</button>
          <div class="mt-3 text-center">
            <router-link to="/login">Login</router-link>
          </div>
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
    return {
      form: { name: '', email: '', password: '', education: '', skills: '', experience: '', contact: '' },
      error: '',
      message: ''
    }
  },
  methods: {
    async register() {
      try {
        const res = await api.post('/api/auth/register/student', this.form)
        this.message = res.data.message
        this.error = ''
        setTimeout(() => this.$router.push('/login'), 1500)
      } catch (err) {
        this.error = err.response?.data?.error || 'Registration failed'
      }
    }
  }
}
</script>