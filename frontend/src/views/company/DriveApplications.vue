<template>
  <div>
    <nav class="navbar border-bottom">
      <div class="container">
        <img src="/logo.svg" height="46" alt="Placement Portal" />
        <router-link to="/company/dashboard" class="btn btn-outline-dark btn-sm">Go Back</router-link>
      </div>
    </nav>

    <div class="container mt-4">
      <h4 class="mb-4">Applications for {{ drive.job_title }}</h4>

      <table class="table table-bordered table-hover">
        <thead class="table-dark">
          <tr>
            <th>Student Name</th><th>Status</th><th>Applied At</th><th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="app in applications" :key="app.id">
            <td>{{ app.student_name }}</td>
            <td>{{ app.status }}</td>
            <td>{{ app.applied_at }}</td>
            <td>
              <button @click="reviewApplication(app.id)" class="btn btn-outline-primary btn-sm me-2">Review</button>
              <button @click="viewStudent(app.student_id)" class="btn btn-outline-secondary btn-sm">Profile</button>
            </td>
          </tr>
        </tbody>
      </table>

      <div v-if="selectedApplication" class="modal d-block" style="background: rgba(0,0,0,0.5);">
        <div class="modal-dialog">
          <div class="modal-content p-4">
            <h5>{{ selectedApplication.student_name }}</h5>
            <p><strong>Email:</strong> {{ selectedApplication.student_email }}</p>
            <p><strong>Education:</strong> {{ selectedApplication.education }}</p>
            <p><strong>Skills:</strong> {{ selectedApplication.skills }}</p>
            <p><strong>Experience:</strong> {{ selectedApplication.experience }}</p>
            <p><strong>Contact:</strong> {{ selectedApplication.contact }}</p>
            <p><strong>Current Status:</strong> {{ selectedApplication.status }}</p>
            <div class="mb-3">
              <label class="form-label">Update Status</label>
              <select v-model="newStatus" class="form-select">
                <option value="Applied">Applied</option>
                <option value="Shortlisted">Shortlisted</option>
                <option value="Interview">Interview</option>
                <option value="Offer">Offer</option>
                <option value="Rejected">Rejected</option>
                <option value="Placed">Placed</option>
              </select>
            </div>
            <div class="d-flex gap-2">
              <button @click="updateStatus" class="btn btn-outline-success btn-sm">Update</button>
              <button @click="selectedApplication = null" class="btn btn-secondary btn-sm">Close</button>
            </div>
          </div>
        </div>
      </div>

      <div v-if="selectedStudent" class="modal d-block" style="background: rgba(0,0,0,0.5);">
  <div class="modal-dialog">
    <div class="modal-content p-4">
      <h5>{{ selectedStudent.name }}</h5>
      <p><strong>Education:</strong> {{ selectedStudent.education }}</p>
      <p><strong>Skills:</strong> {{ selectedStudent.skills }}</p>
      <p><strong>Experience:</strong> {{ selectedStudent.experience }}</p>
      <p><strong>Contact:</strong> {{ selectedStudent.contact }}</p>
      <h6 class="mt-3">Applications</h6>
      <div v-for="a in selectedStudent.applications" :key="a.drive_id" class="border rounded p-2 mb-1">
        <span>{{ a.job_title }} | {{ a.status }} | {{ a.applied_at }}</span>
      </div>
      <button @click="selectedStudent = null" class="btn btn-secondary btn-sm mt-2">Close</button>
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
      drive: {},
      applications: [],
      selectedApplication: null,
      newStatus: '',
      selectedStudent: null
    }
  },
  mounted() {
    this.fetchApplications()
  },
  methods: {
    async fetchApplications() {
      const drive_id = this.$route.params.drive_id
      const res = await api.get(`/api/company/drives/${drive_id}/applications`)
      this.drive = res.data.drive
      this.applications = res.data.applications
    },
    async reviewApplication(id) {
      const res = await api.get(`/api/company/applications/${id}`)
      this.selectedApplication = res.data
      this.newStatus = res.data.status
    },
    async viewStudent(student_id) {
    const res = await api.get(`/api/company/students/${student_id}`)
    this.selectedStudent = res.data
    },
    async updateStatus() {
      await api.post(`/api/company/applications/${this.selectedApplication.application_id}/status`, { status: this.newStatus })
      this.selectedApplication = null
      this.fetchApplications()
    }
  }
}
</script>