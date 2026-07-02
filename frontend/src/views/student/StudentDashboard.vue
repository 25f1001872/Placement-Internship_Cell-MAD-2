<template>
  <div>
    <nav class="navbar border-bottom">
      <div class="container">
        <span class="navbar-brand fw-semibold">Placement Portal | Student</span>
        <div class="d-flex gap-2">
          <button @click="tab = 'profile'" class="btn btn-outline-primary btn-sm">Profile</button>
          <button @click="logout" class="btn btn-outline-dark btn-sm">Logout</button>
        </div>
      </div>
    </nav>

    <div class="container mt-4">
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h4>Welcome {{ student_name }}</h4>
      </div>

      <div v-if="error" class="alert alert-danger">{{ error }}</div>

      <ul class="nav nav-tabs mb-4">
        <li class="nav-item">
          <a class="nav-link" :class="{ active: tab === 'companies' }" href="#" @click.prevent="tab = 'companies'">Organizations</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" :class="{ active: tab === 'drives' }" href="#" @click.prevent="tab = 'drives'">Browse Drives</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" :class="{ active: tab === 'applications' }" href="#" @click.prevent="tab = 'applications'">My Applications</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" :class="{ active: tab === 'profile' }" href="#" @click.prevent="tab = 'profile'">Profile</a>
        </li>
      </ul>

      <div v-if="tab === 'companies'">
        <div class="border rounded p-3">
          <div v-for="c in companies" :key="c.id" class="row align-items-center border-bottom py-2">
            <div class="col-md-8 fw-semibold">{{ c.name }}</div>
            <div class="col-md-4 text-end">
              <button @click="viewDrives(c.id)" class="btn btn-outline-dark btn-sm">View Drives</button>
            </div>
          </div>
        </div>
      </div>

      <div v-if="tab === 'drives'">
        <div class="row mb-3 g-2">
          <div class="col-md-3">
            <input v-model="search.company" type="text" class="form-control" placeholder="Search by company" @input="fetchDrives" />
          </div>
          <div class="col-md-3">
            <input v-model="search.position" type="text" class="form-control" placeholder="Search by position" @input="fetchDrives" />
          </div>
          <div class="col-md-3">
            <input v-model="search.skills" type="text" class="form-control" placeholder="Search by skills" @input="fetchDrives" />
          </div>
        </div>
        <table class="table table-bordered table-hover">
          <thead class="table-dark">
            <tr>
              <th>Company</th><th>Job Title</th><th>Skills</th><th>Salary</th><th>Deadline</th><th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="d in drives" :key="d.id">
              <td>{{ d.company_name }}</td>
              <td>{{ d.job_title }}</td>
              <td>{{ d.skills_required }}</td>
              <td>{{ d.salary }}</td>
              <td>{{ d.deadline }}</td>
              <td>
                <button @click="viewDrive(d.id)" class="btn btn-outline-primary btn-sm">View & Apply</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div v-if="tab === 'applications'">
        <table class="table table-bordered table-hover">
          <thead class="table-dark">
            <tr>
              <th>Job Title</th><th>Company</th><th>Status</th><th>Applied At</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="a in applications" :key="a.id">
              <td>{{ a.job_title }}</td>
              <td>{{ a.company_name }}</td>
              <td>{{ a.status }}</td>
              <td>{{ a.applied_at }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div v-if="tab === 'profile'">
        <div v-if="profileMessage" class="alert alert-success">{{ profileMessage }}</div>
        <div class="mb-3">
          <label class="form-label">Education</label>
          <input v-model="profile.education" type="text" class="form-control" />
        </div>
        <div class="mb-3">
          <label class="form-label">Skills</label>
          <input v-model="profile.skills" type="text" class="form-control" />
        </div>
        <div class="mb-3">
          <label class="form-label">Experience</label>
          <input v-model="profile.experience" type="text" class="form-control" />
        </div>
        <div class="mb-3">
          <label class="form-label">Contact</label>
          <input v-model="profile.contact" type="text" class="form-control" />
        </div>
        <button @click="updateProfile" class="btn btn-outline-success btn-sm">Update Profile</button>
      </div>

      <div v-if="selectedDrive" class="modal d-block" style="background: rgba(0,0,0,0.5);">
        <div class="modal-dialog">
          <div class="modal-content p-4">
            <h5>{{ selectedDrive.job_title }}</h5>
            <p><strong>Company:</strong> {{ selectedDrive.company_name }}</p>
            <p><strong>Description:</strong> {{ selectedDrive.job_description }}</p>
            <p><strong>Skills Required:</strong> {{ selectedDrive.skills_required }}</p>
            <p><strong>Eligibility:</strong> {{ selectedDrive.eligibility }}</p>
            <p><strong>Salary:</strong> {{ selectedDrive.salary }}</p>
            <p><strong>Benefits:</strong> {{ selectedDrive.benefits }}</p>
            <p><strong>Deadline:</strong> {{ selectedDrive.deadline }}</p>
            <p><strong>Status:</strong> {{ selectedDrive.status }}</p>
            <div v-if="applyMessage" class="alert alert-success">{{ applyMessage }}</div>
            <div v-if="applyError" class="alert alert-danger">{{ applyError }}</div>
            <div class="d-flex gap-2">
              <button v-if="!selectedDrive.already_applied && selectedDrive.status === 'Active'" @click="applyDrive(selectedDrive.id)" class="btn btn-outline-success btn-sm">Apply</button>
              <span v-if="selectedDrive.already_applied" class="btn btn-secondary btn-sm disabled">Already Applied</span>
              <button @click="selectedDrive = null" class="btn btn-secondary btn-sm">Close</button>
            </div>
          </div>
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
      tab: 'companies',
      student_name: '',
      companies: [],
      drives: [],
      applications: [],
      selectedDrive: null,
      profile: { education: '', skills: '', experience: '', contact: '' },
      search: { company: '', position: '', skills: '' },
      error: '',
      applyMessage: '',
      applyError: '',
      profileMessage: ''
    }
  },
  mounted() {
    this.fetchDashboard()
    this.fetchDrives()
    this.fetchApplications()
    this.fetchProfile()
  },
  methods: {
    async fetchDashboard() {
      try {
        const res = await api.get('/api/student/dashboard')
        this.student_name = res.data.student_name
        this.companies = res.data.companies
      } catch (err) {
        this.error = err.response?.data?.error || 'Failed to load dashboard'
      }
    },
    async fetchDrives() {
      const res = await api.get('/api/student/drives', { params: { company: this.search.company, position: this.search.position, skills: this.search.skills } })
      this.drives = res.data
    },
    async fetchApplications() {
      const res = await api.get('/api/student/applications')
      this.applications = res.data
    },
    async fetchProfile() {
      const res = await api.get('/api/student/profile')
      this.profile = res.data
    },
    async viewDrive(id) {
      const res = await api.get(`/api/student/drives/${id}`)
      this.selectedDrive = res.data
      this.applyMessage = ''
      this.applyError = ''
      this.tab = 'drives'
    },
    async applyDrive(id) {
      try {
        const res = await api.post(`/api/student/drives/${id}/apply`)
        this.applyMessage = res.data.message
        this.applyError = ''
        this.selectedDrive.already_applied = true
        this.fetchApplications()
        this.fetchDashboard()
      } catch (err) {
        this.applyError = err.response?.data?.error || 'Failed to apply'
      }
    },
    viewDrives(company_id) {
      this.search.company = this.companies.find(c => c.id === company_id)?.name || ''
      this.fetchDrives()
      this.tab = 'drives'
    },
    async updateProfile() {
      await api.put('/api/student/profile', this.profile)
      this.profileMessage = 'Profile updated successfully'
    },
    logout() {
      localStorage.clear()
      this.$router.push('/login')
    }
  }
}
</script>