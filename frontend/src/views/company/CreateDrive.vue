<template>
  <div>
    <nav class="navbar border-bottom">
      <div class="container">
        <img src="/logo.svg" height="46" alt="Placement Portal" />
        <router-link to="/company/dashboard" class="btn btn-outline-dark btn-sm">Back</router-link>
      </div>
    </nav>

    <div class="container mt-4">
      <h4 class="mb-4">Create a Placement Drive</h4>

      <div v-if="error" class="alert alert-danger">{{ error }}</div>
      <div v-if="message" class="alert alert-success">{{ message }}</div>

      <div class="mb-3">
        <label class="form-label">Job Title</label>
        <input v-model="form.job_title" type="text" class="form-control" />
      </div>
      <div class="mb-3">
        <label class="form-label">Job Description</label>
        <textarea v-model="form.job_description" class="form-control" rows="3"></textarea>
      </div>
      <div class="mb-3">
        <label class="form-label">Eligibility Criteria</label>
        <textarea v-model="form.eligibility" class="form-control" rows="2"></textarea>
      </div>
      <div class="mb-3">
        <label class="form-label">Skills Required</label>
        <input v-model="form.skills_required" type="text" class="form-control" />
      </div>
      <div class="mb-3">
        <label class="form-label">Salary</label>
        <input v-model="form.salary" type="text" class="form-control" />
      </div>
      <div class="mb-3">
        <label class="form-label">Benefits</label>
        <input v-model="form.benefits" type="text" class="form-control" />
      </div>
      <div class="mb-3">
        <label class="form-label">Application Deadline</label>
        <input v-model="form.deadline" type="date" class="form-control" />
      </div>
      <div class="d-flex justify-content-end">
        <button @click="createDrive" class="btn btn-outline-success">Create Drive</button>
      </div>

    </div>
  </div>
</template>

<script>
import api from '../../utils/api'

export default {
  data() {
    return {
      form: { job_title: '', job_description: '', eligibility: '', skills_required: '', salary: '', benefits: '', deadline: '' },
      error: '',
      message: ''
    }
  },
  methods: {
    async createDrive() {
      try {
        const res = await api.post('/api/company/drives', this.form)
        this.message = res.data.message
        this.error = ''
        setTimeout(() => this.$router.push('/company/dashboard'), 1500)
      } catch (err) {
        this.error = err.response?.data?.error || 'Failed to create drive'
      }
    }
  }
}
</script>