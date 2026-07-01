<template>
  <div>
    <nav class="navbar navbar-expand-lg border-bottom">
      <div class="container">
        <a class="navbar-brand d-flex align-items-center gap-2" href="#">
          <span class="fw-semibold">Placement Portal</span>
        </a>
        <div class="ms-auto">
          <router-link to="/login" class="btn btn-outline-dark btn-sm">Login</router-link>
        </div>
      </div>
    </nav>

    <div class="container py-5 d-flex justify-content-center">
      <div class="card shadow-sm p-5 text-center" style="max-width: 1200px; width: 100%;">
        <div class="text-center mb-3 mt-3">
          <h2 class="display-5 fw-bold text-dark">IIT Madras Placement Portal</h2>
          <p class="mt-3 text-muted mx-auto lead" style="max-width: 650px;">
            Connecting India's brightest minds with global industry leaders. Explore job opportunities, internships, and career resources.
          </p>
        </div>
        <div class="row g-4 justify-content-center">
          <div class="col-md-5">
            <div class="card h-100 p-4">
              <div class="card-body d-flex flex-column text-center">
                <div class="mb-3 fs-1">📚🎓🏫👨🏻‍🎓🎒</div>
                <h3 class="fw-bold mb-3">Students</h3>
                <p class="text-muted flex-grow-1">Access job boards, create your profile, prepare for interviews, and track your applications.</p>
                <div class="d-grid gap-2 mt-4">
                  <router-link to="/login" class="btn btn-dark py-2 rounded-3">Sign in as Student</router-link>
                  <router-link to="/register/student" class="btn btn-outline-secondary py-2 rounded-3">New Registration</router-link>
                </div>
              </div>
            </div>
          </div>
          <div class="col-md-5">
            <div class="card h-100 p-4">
              <div class="card-body d-flex flex-column text-center">
                <div class="mb-3 fs-1">🏢🏛️</div>
                <h3 class="fw-bold mb-3">Recruiters</h3>
                <p class="text-muted flex-grow-1">Hire the best talent. Post job openings, schedule campus visits, and manage interviews.</p>
                <div class="d-grid gap-2 mt-4">
                  <router-link to="/login" class="btn btn-dark py-2 rounded-3">Sign in as Recruiter</router-link>
                  <router-link to="/register/company" class="btn btn-outline-secondary py-2 rounded-3">Register Company</router-link>
                </div>
              </div>
            </div>
          </div>
        </div>
        <br>
      </div>
    </div>
  </div>
</template>

<script>
export default {
}
</script>