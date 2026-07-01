<template>
  <div>
    <nav class="navbar navbar-expand-lg border-bottom">
      <div class="container">
        <span class="navbar-brand fw-semibold">Placement Portal | Admin</span>
        <div class="ms-auto">
          <button @click="logout" class="btn btn-outline-dark btn-sm">Logout</button>
        </div>
      </div>
    </nav>

    <div class="container mt-4">
      <h4 class="mb-4">Admin Dashboard</h4>

      <div class="row g-3 mb-4">
        <div class="col-md-3">
          <div class="card text-center p-3">
            <h6 class="text-muted">Students</h6>
            <h3>{{ stats.total_students }}</h3>
          </div>
        </div>
        <div class="col-md-3">
          <div class="card text-center p-3">
            <h6 class="text-muted">Companies</h6>
            <h3>{{ stats.total_companies }}</h3>
          </div>
        </div>
        <div class="col-md-3">
          <div class="card text-center p-3">
            <h6 class="text-muted">Drives</h6>
            <h3>{{ stats.total_drives }}</h3>
          </div>
        </div>
        <div class="col-md-3">
          <div class="card text-center p-3">
            <h6 class="text-muted">Applications</h6>
            <h3>{{ stats.total_applications }}</h3>
          </div>
        </div>
      </div>

      <ul class="nav nav-tabs mb-4">
        <li class="nav-item">
          <a class="nav-link" :class="{ active: tab === 'companies' }" href="#" @click.prevent="tab = 'companies'">Companies</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" :class="{ active: tab === 'students' }" href="#" @click.prevent="tab = 'students'">Students</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" :class="{ active: tab === 'drives' }" href="#" @click.prevent="tab = 'drives'">Drives</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" :class="{ active: tab === 'applications' }" href="#" @click.prevent="tab = 'applications'">Applications</a>
        </li>
      </ul>

      <div v-if="tab === 'companies'">
        <div class="row mb-3 g-2">
          <div class="col-md-4">
            <input v-model="search.company_name" type="text" class="form-control" placeholder="Search by name" @input="fetchCompanies" />
          </div>
          <div class="col-md-4">
            <input v-model="search.industry" type="text" class="form-control" placeholder="Search by industry" @input="fetchCompanies" />
          </div>
        </div>
        <table class="table table-bordered table-hover">
          <thead class="table-dark">
            <tr>
              <th>Name</th><th>Industry</th><th>Location</th><th>Status</th><th>Blacklisted</th><th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="c in companies" :key="c.id">
              <td>{{ c.name }}</td>
              <td>{{ c.industry }}</td>
              <td>{{ c.location }}</td>
              <td>{{ c.approval_status }}</td>
              <td>{{ c.is_blacklisted ? 'Yes' : 'No' }}</td>
              <td class="d-flex gap-1">
                <button v-if="c.approval_status === 'Pending'" @click="approveCompany(c.id)" class="btn btn-success btn-sm">Approve</button>
                <button v-if="c.approval_status === 'Pending'" @click="rejectCompany(c.id)" class="btn btn-danger btn-sm">Reject</button>
                <button @click="blacklistCompany(c.id)" class="btn btn-warning btn-sm">{{ c.is_blacklisted ? 'Unblacklist' : 'Blacklist' }}</button>
                <button @click="viewCompany(c.id)" class="btn btn-outline-secondary btn-sm">View</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div v-if="tab === 'students'">
        <div class="row mb-3 g-2">
          <div class="col-md-3">
            <input v-model="search.student_name" type="text" class="form-control" placeholder="Search by name" @input="fetchStudents" />
          </div>
          <div class="col-md-3">
            <input v-model="search.student_id" type="text" class="form-control" placeholder="Search by ID" @input="fetchStudents" />
          </div>
          <div class="col-md-3">
            <input v-model="search.contact" type="text" class="form-control" placeholder="Search by contact" @input="fetchStudents" />
          </div>
        </div>
        <table class="table table-bordered table-hover">
          <thead class="table-dark">
            <tr>
              <th>ID</th><th>Name</th><th>Email</th><th>Skills</th><th>Blacklisted</th><th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="s in students" :key="s.id">
              <td>{{ s.id }}</td>
              <td>{{ s.name }}</td>
              <td>{{ s.email }}</td>
              <td>{{ s.skills }}</td>
              <td>{{ s.is_blacklisted ? 'Yes' : 'No' }}</td>
              <td class="d-flex gap-1">
                <button @click="blacklistStudent(s.id)" class="btn btn-warning btn-sm">{{ s.is_blacklisted ? 'Unblacklist' : 'Blacklist' }}</button>
                <button @click="viewStudent(s.id)" class="btn btn-outline-secondary btn-sm">View</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div v-if="tab === 'drives'">
        <table class="table table-bordered table-hover">
          <thead class="table-dark">
            <tr>
              <th>Company</th><th>Job Title</th><th>Deadline</th><th>Status</th><th>Approval</th><th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="d in drives" :key="d.id">
              <td>{{ d.company_name }}</td>
              <td>{{ d.job_title }}</td>
              <td>{{ d.deadline }}</td>
              <td>{{ d.status }}</td>
              <td>{{ d.approval_status }}</td>
              <td class="d-flex gap-1">
                <button v-if="d.approval_status === 'Pending'" @click="approveDrive(d.id)" class="btn btn-success btn-sm">Approve</button>
                <button v-if="d.approval_status === 'Pending'" @click="rejectDrive(d.id)" class="btn btn-danger btn-sm">Reject</button>
                <button v-if="d.status === 'Active'" @click="closeDrive(d.id)" class="btn btn-warning btn-sm">Close</button>
                <button @click="viewDrive(d.id)" class="btn btn-outline-secondary btn-sm">View</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div v-if="tab === 'applications'">
        <table class="table table-bordered table-hover">
          <thead class="table-dark">
            <tr>
              <th>Student</th><th>Company</th><th>Job Title</th><th>Status</th><th>Applied At</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="a in applications" :key="a.id">
              <td>{{ a.student_name }}</td>
              <td>{{ a.company_name }}</td>
              <td>{{ a.job_title }}</td>
              <td>{{ a.status }}</td>
              <td>{{ a.applied_at }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div v-if="selectedCompany" class="modal d-block" style="background: rgba(0,0,0,0.5);">
        <div class="modal-dialog modal-lg">
          <div class="modal-content p-4">
            <h5>{{ selectedCompany.name }}</h5>
            <p><strong>Email:</strong> {{ selectedCompany.email }}</p>
            <p><strong>Industry:</strong> {{ selectedCompany.industry }}</p>
            <p><strong>Location:</strong> {{ selectedCompany.location }}</p>
            <p><strong>Website:</strong> {{ selectedCompany.website }}</p>
            <p><strong>Description:</strong> {{ selectedCompany.company_description }}</p>
            <p><strong>Status:</strong> {{ selectedCompany.approval_status }}</p>
            <h6 class="mt-3">Drives</h6>
            <table class="table table-sm table-bordered">
              <thead><tr><th>Title</th><th>Status</th><th>Approval</th><th>Deadline</th></tr></thead>
              <tbody>
                <tr v-for="d in selectedCompany.drives" :key="d.id">
                  <td>{{ d.job_title }}</td><td>{{ d.status }}</td><td>{{ d.approval_status }}</td><td>{{ d.deadline }}</td>
                </tr>
              </tbody>
            </table>
            <button @click="selectedCompany = null" class="btn btn-secondary mt-2">Close</button>
          </div>
        </div>
      </div>

      <div v-if="selectedStudent" class="modal d-block" style="background: rgba(0,0,0,0.5);">
        <div class="modal-dialog">
          <div class="modal-content p-4">
            <h5>{{ selectedStudent.name }}</h5>
            <p><strong>Email:</strong> {{ selectedStudent.email }}</p>
            <p><strong>Education:</strong> {{ selectedStudent.education }}</p>
            <p><strong>Skills:</strong> {{ selectedStudent.skills }}</p>
            <p><strong>Experience:</strong> {{ selectedStudent.experience }}</p>
            <p><strong>Contact:</strong> {{ selectedStudent.contact }}</p>
            <h6 class="mt-3">Applications</h6>
            <table class="table table-sm table-bordered">
              <thead><tr><th>Drive ID</th><th>Status</th><th>Applied At</th></tr></thead>
              <tbody>
                <tr v-for="a in selectedStudent.applications" :key="a.id">
                  <td>{{ a.drive_id }}</td><td>{{ a.status }}</td><td>{{ a.applied_at }}</td>
                </tr>
              </tbody>
            </table>
            <button @click="selectedStudent = null" class="btn btn-secondary mt-2">Close</button>
          </div>
        </div>
      </div>

      <div v-if="selectedDrive" class="modal d-block" style="background: rgba(0,0,0,0.5);">
        <div class="modal-dialog modal-lg">
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
            <h6 class="mt-3">Applications</h6>
            <table class="table table-sm table-bordered">
              <thead><tr><th>Student</th><th>Status</th><th>Applied At</th></tr></thead>
              <tbody>
                <tr v-for="a in selectedDrive.applications" :key="a.id">
                  <td>{{ a.student_name }}</td><td>{{ a.status }}</td><td>{{ a.applied_at }}</td>
                </tr>
              </tbody>
            </table>
            <button @click="selectedDrive = null" class="btn btn-secondary mt-2">Close</button>
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
      stats: {},
      companies: [],
      students: [],
      drives: [],
      applications: [],
      selectedCompany: null,
      selectedStudent: null,
      selectedDrive: null,
      search: { company_name: '', industry: '', student_name: '', student_id: '', contact: '' }
    }
  },
  mounted() {
    this.fetchStats()
    this.fetchCompanies()
    this.fetchStudents()
    this.fetchDrives()
    this.fetchApplications()
  },
  methods: {
    async fetchStats() {
      const res = await api.get('/api/admin/dashboard')
      this.stats = res.data
    },
    async fetchCompanies() {
      const res = await api.get('/api/admin/companies', { params: { name: this.search.company_name, industry: this.search.industry } })
      this.companies = res.data
    },
    async fetchStudents() {
      const res = await api.get('/api/admin/students', { params: { name: this.search.student_name, id: this.search.student_id, contact: this.search.contact } })
      this.students = res.data
    },
    async fetchDrives() {
      const res = await api.get('/api/admin/drives')
      this.drives = res.data
    },
    async fetchApplications() {
      const res = await api.get('/api/admin/applications')
      this.applications = res.data
    },
    async approveCompany(id) {
      await api.post(`/api/admin/companies/${id}/approve`)
      this.fetchCompanies()
      this.fetchStats()
    },
    async rejectCompany(id) {
      await api.post(`/api/admin/companies/${id}/reject`)
      this.fetchCompanies()
      this.fetchStats()
    },
    async blacklistCompany(id) {
      await api.post(`/api/admin/companies/${id}/blacklist`)
      this.fetchCompanies()
    },
    async approveStudent(id) {
      await api.post(`/api/admin/students/${id}/approve`)
      this.fetchStudents()
    },
    async blacklistStudent(id) {
      await api.post(`/api/admin/students/${id}/blacklist`)
      this.fetchStudents()
    },
    async approveDrive(id) {
      await api.post(`/api/admin/drives/${id}/approve`)
      this.fetchDrives()
      this.fetchStats()
    },
    async rejectDrive(id) {
      await api.post(`/api/admin/drives/${id}/reject`)
      this.fetchDrives()
    },
    async closeDrive(id) {
      await api.post(`/api/admin/drives/${id}/close`)
      this.fetchDrives()
    },
    async viewCompany(id) {
      const res = await api.get(`/api/admin/companies/${id}`)
      this.selectedCompany = res.data
    },
    async viewStudent(id) {
      const res = await api.get(`/api/admin/students/${id}`)
      this.selectedStudent = res.data
    },
    async viewDrive(id) {
      const res = await api.get(`/api/admin/drives/${id}`)
      this.selectedDrive = res.data
    },
    logout() {
      localStorage.clear()
      this.$router.push('/login')
    }
  }
}
</script>