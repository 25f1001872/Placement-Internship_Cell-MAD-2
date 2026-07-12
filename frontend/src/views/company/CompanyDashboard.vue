<template>
  <div>
    <nav class="navbar border-bottom">
      <div class="container">
        <img src="/logo.svg" height="46" alt="Placement Portal" />
        <button @click="logout" class="btn btn-outline-dark btn-sm">Logout</button>
      </div>
    </nav>

    <div class="container mt-4">
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h4>Welcome {{ company_name }}</h4>
        <router-link to="/company/create-drive" class="btn btn-outline-primary btn-sm">Create New Drive</router-link>
      </div>

      <div v-if="error" class="alert alert-danger">{{ error }}</div>

      <ul class="nav nav-tabs mb-4">
        <li class="nav-item">
          <a class="nav-link" :class="{ active: tab === 'upcoming' }" href="#" @click.prevent="tab = 'upcoming'">Upcoming Drives</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" :class="{ active: tab === 'closed' }" href="#" @click.prevent="tab = 'closed'">Closed Drives</a>
        </li>
      </ul>

      <div v-if="tab === 'upcoming'">
        <table class="table table-bordered table-hover">
          <thead class="table-dark">
            <tr>
              <th>Drive ID</th><th>Job Title</th><th>Deadline</th><th>Approval</th><th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="d in upcoming_drives" :key="d.id">
              <td>{{ d.id }}</td>
              <td>{{ d.job_title }}</td>
              <td>{{ d.deadline }}</td>
              <td>{{ d.approval_status }}</td>
              <td class="d-flex gap-1">
                <button @click="viewApplications(d.id)" class="btn btn-outline-primary btn-sm">View Details</button>
                <button @click="closeDrive(d.id)" class="btn btn-outline-success btn-sm">Mark as Complete</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div v-if="tab === 'closed'">
        <table class="table table-bordered table-hover">
          <thead class="table-dark">
            <tr>
              <th>Drive ID</th><th>Job Title</th><th>Deadline</th><th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="d in closed_drives" :key="d.id">
              <td>{{ d.id }}</td>
              <td>{{ d.job_title }}</td>
              <td>{{ d.deadline }}</td>
              <td>
                <button @click="viewApplications(d.id)" class="btn btn-outline-dark btn-sm">View Details</button>
              </td>
            </tr>
          </tbody>
        </table>
      <div class="mt-3">
  <button @click="exportCSV" class="btn btn-outline-secondary btn-sm">Export Applications (CSV)</button>
      </div>
      </div>


    </div>
  </div>
</template>

<script>
import api from '../../utils/api'

export default {
  data() {
    return {
      tab: 'upcoming',
      company_name: '',
      upcoming_drives: [],
      closed_drives: [],
      error: ''
    }
  },
  mounted() {
    this.fetchDashboard()
  },
  methods: {
    async fetchDashboard() {
      try {
        const res = await api.get('/api/company/dashboard')
        this.company_name = res.data.company_name
        this.upcoming_drives = res.data.upcoming_drives
        this.closed_drives = res.data.closed_drives
      } catch (err) {
        this.error = err.response?.data?.error || 'Failed to load dashboard'
      }
    },
    async closeDrive(id) {
      await api.post(`/api/company/drives/${id}/close`)
      this.fetchDashboard()
    },
    async exportCSV() {
  const res = await api.get('/api/tasks/export/company', { responseType: 'blob' })
  const url = window.URL.createObjectURL(new Blob([res.data]))
  const link = document.createElement('a')
  link.href = url
  link.setAttribute('download', 'company_applications.csv')
  document.body.appendChild(link)
  link.click()
},
    viewApplications(id) {
      this.$router.push(`/company/drives/${id}/applications`)
    },
    logout() {
      localStorage.clear()
      this.$router.push('/login')
    }
  }
}
</script>