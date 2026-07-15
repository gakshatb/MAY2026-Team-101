import { createRouter, createWebHistory } from 'vue-router'

// --- Public Imports ---
import LandingPage from '../views/public/LandingPage.vue'
import About from '../views/public/About.vue'
import Services from '../views/public/Services.vue'
import HowItWorks from '../views/public/HowItWorks.vue'
import Contact from '../views/public/Contact.vue'
import FAQs from '../views/public/FAQs.vue'

// --- Auth Imports ---
import Login from '../views/auth/Login.vue'
import Register from '../views/auth/Register.vue'
import ForgotPassword from '../views/auth/ForgotPassword.vue'

// --- Citizen Imports ---
import Dashboard from '../views/citizen/Dashboard.vue'
import Profile from '../views/citizen/Profile.vue'
import Notifications from '../views/citizen/Notifications.vue'
import MyComplaints from '../views/citizen/MyComplaints.vue'
import SubmitComplaint from '../views/citizen/SubmitComplaint.vue'
import ComplaintDetails from '../views/citizen/ComplaintDetails.vue'
import ComplaintTracking from '../views/citizen/ComplaintTracking.vue'
import Feedback from '../views/citizen/Feedback.vue'

// --- Officer Imports ---
import OfficerDashboard from '../views/officer/Dashboard.vue'
import AnalyticsReports from '../views/officer/AnalyticsReports.vue'
import AssignWorker from '../views/officer/AssignWorker.vue'
import OfficerComplaintDetails from '../views/officer/ComplaintDetails.vue'
import ComplaintManagement from '../views/officer/ComplaintManagement.vue'
import ManageWorkers from '../views/officer/ManageWorkers.vue'
import OfficerNotifications from '../views/officer/Notifications.vue'
import OfficerProfile from '../views/officer/Profile.vue'

// --- Worker Imports ---
import WorkerDashboard from '../views/worker/Dashboard.vue'
import WorkerAssignedTasks from '../views/worker/AssignedTasks.vue'
import WorkerTaskDetails from '../views/worker/TaskDetails.vue'
import WorkerUpdateComplaint from '../views/worker/UpdateComplaint.vue'
import WorkerCompletedTasks from '../views/worker/CompletedTasks.vue'
import WorkerNotifications from '../views/worker/Notifications.vue'
import WorkerProfile from '../views/worker/Profile.vue'
import DepartmentApplications from '../views/worker/DepartmentApplications.vue'

// --- Admin Imports ---
import AdminDashboard from '../views/admin/Dashboard.vue'
import DepartmentManagement from '../views/admin/DepartmentManagement.vue'
import OfficerDetails from '../views/admin/OfficerDetails.vue'
import OfficerManagement from '../views/admin/OfficerManagement.vue'
import OfficersProfile from '../views/admin/Profile.vue'
import SystemAnalytics from '../views/admin/SystemAnalytics.vue'
import ActivityLogs from '../views/admin/ActivityLogs.vue'
import Announcements from '../views/admin/Announcements.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    // --- Public Routes ---
    { path: '/', name: 'Home', component: LandingPage, meta: { title: 'CivicDesk | Home', guestOnly: true } },
    { path: '/about', name: 'About', component: About, meta: { title: 'About | CivicDesk' } },
    { path: '/services', name: 'Services', component: Services, meta: { title: 'Services | CivicDesk' } },
    { path: '/how-it-works', name: 'HowItWorks', component: HowItWorks, meta: { title: 'How It Works | CivicDesk' } },
    { path: '/contact', name: 'Contact', component: Contact, meta: { title: 'Contact Us | CivicDesk' } },
    { path: '/faq', name: 'FAQs', component: FAQs, meta: { title: 'FAQs | CivicDesk' } },

    // --- Auth Routes ---
    { path: '/login', name: 'Login', component: Login, meta: { title: 'Login | CivicDesk', guestOnly: true } },
    { path: '/register', name: 'Register', component: Register, meta: { title: 'Register | CivicDesk', guestOnly: true } },
    { path: '/forgot-password', name: 'ForgotPassword', component: ForgotPassword, meta: { title: 'Reset Password | CivicDesk', guestOnly: true } },

    // --- Citizen Routes ---
    { path: '/citizen/dashboard', name: 'CitizenDashboard', component: Dashboard, meta: { title: 'Dashboard | CivicDesk', requiresAuth: true } },
    { path: '/citizen/profile', name: 'CitizenProfile', component: Profile, meta: { title: 'Profile | CivicDesk', requiresAuth: true } },
    { path: '/citizen/notifications', name: 'CitizenNotifications', component: Notifications, meta: { title: 'Notifications | CivicDesk', requiresAuth: true } },
    { path: '/citizen/complaints', name: 'MyComplaints', component: MyComplaints, meta: { title: 'My Complaints | CivicDesk', requiresAuth: true } },
    { path: '/citizen/submit', name: 'SubmitComplaint', component: SubmitComplaint, meta: { title: 'Submit Complaint | CivicDesk', requiresAuth: true } },
    { path: '/citizen/complaintdetails/:id', name: 'ComplaintDetails', component: ComplaintDetails, meta: { title: 'Details | CivicDesk', requiresAuth: true }, props: true },
    { path: '/citizen/track/:id', name: 'ComplaintTracking', component: ComplaintTracking, meta: { title: 'Track | CivicDesk', requiresAuth: true }, props: true },
    { path: '/citizen/feedback/:id', name: 'CitizenFeedback', component: Feedback, meta: { title: 'Feedback | CivicDesk', requiresAuth: true }, props: true },

    // --- Officer Routes ---
    { path: '/officer/dashboard', name: 'OfficerDashboard', component: OfficerDashboard, meta: { title: 'Officer Dashboard | CivicDesk', requiresAuth: true } },
    { path: '/officer/complaints', name: 'OfficerComplaintManagement', component: ComplaintManagement, meta: { title: 'Complaint Management | CivicDesk', requiresAuth: true } },
    { path: '/officer/complaintdetails/:id', name: 'OfficerComplaintDetails', component: OfficerComplaintDetails, meta: { title: 'Complaint Details | CivicDesk', requiresAuth: true }, props: true },
    { path: '/officer/workers', name: 'ManageWorkers', component: ManageWorkers, meta: { title: 'Manage Workers | CivicDesk', requiresAuth: true } },
    { path: '/officer/assign/:id', name: 'AssignWorker', component: AssignWorker, meta: { title: 'Assign Worker | CivicDesk', requiresAuth: true }, props: true },
    { path: '/officer/analytics', name: 'AnalyticsReports', component: AnalyticsReports, meta: { title: 'Analytics | CivicDesk', requiresAuth: true } },
    { path: '/officer/notifications', name: 'OfficerNotifications', component: OfficerNotifications, meta: { title: 'Notifications | CivicDesk', requiresAuth: true } },
    { path: '/officer/profile', name: 'OfficerProfile', component: OfficerProfile, meta: { title: 'Profile | CivicDesk', requiresAuth: true } },

    // --- Worker Routes ---
    { path: '/worker/dashboard', name: 'WorkerDashboard', component: WorkerDashboard, meta: { title: 'Worker Dashboard | CivicDesk', requiresAuth: true } },
    { path: '/worker/tasks', name: 'WorkerAssignedTasks', component: WorkerAssignedTasks, meta: { title: 'Assigned Tasks | CivicDesk', requiresAuth: true } },
    { path: '/worker/task/:id', name: 'WorkerTaskDetails', component: WorkerTaskDetails, meta: { title: 'Task Details | CivicDesk', requiresAuth: true }, props: true },
    { path: '/worker/update/:id', name: 'WorkerUpdateComplaint', component: WorkerUpdateComplaint, meta: { title: 'Update Complaint | CivicDesk', requiresAuth: true }, props: true },
    { path: '/worker/completed', name: 'WorkerCompletedTasks', component: WorkerCompletedTasks, meta: { title: 'Completed Tasks | CivicDesk', requiresAuth: true } },
    { path: '/worker/notifications', name: 'WorkerNotifications', component: WorkerNotifications, meta: { title: 'Notifications | CivicDesk', requiresAuth: true } },
    { path: '/worker/profile', name: 'WorkerProfile', component: WorkerProfile, meta: { title: 'Profile | CivicDesk', requiresAuth: true } },
    { path: '/worker/departmentapplications', name: 'DepartmentApplications', component: DepartmentApplications, meta: { title: 'Department Applications | CivicDesk', requiresAuth: true } },

    // --- Admin Routes ---
    { path: '/admin/dashboard', name: 'AdminDashboard', component: AdminDashboard, meta: { title: 'Admin Dashboard | CivicDesk', requiresAuth: true } },
    { path: '/admin/departmentmanagement', name: 'DepartmentManagement', component: DepartmentManagement, meta: { title: 'Department Management | CivicDesk', requiresAuth: true } },
    { path: '/admin/officerdetails', name: 'OfficerDetails', component: OfficerDetails, meta: { title: 'Officer Details | CivicDesk', requiresAuth: true } },
    { path: '/admin/officermanagement', name: 'OfficerManagement', component: OfficerManagement, meta: { title: 'Officer Management | CivicDesk', requiresAuth: true } },
    { path: '/admin/profile', name: 'OfficersProfile', component: OfficersProfile, meta: { title: 'Profile | CivicDesk', requiresAuth: true } },
    { path: '/admin/systemanalytics', name: 'SystemAnalytics', component: SystemAnalytics, meta: { title: 'System Analytics | CivicDesk', requiresAuth: true } },
    { path: '/admin/activitylogs', name: 'ActivityLogs', component: ActivityLogs, meta: { title: 'Activity Logs | CivicDesk', requiresAuth: true } },
    { path: '/admin/announcements', name: 'Announcements', component: Announcements, meta: { title: 'Announcements | CivicDesk', requiresAuth: true } },

    // --- Fallback ---
    { path: '/:pathMatch(.*)*', redirect: '/' }
  ],
  scrollBehavior(to, from, savedPosition) {
    return savedPosition || { top: 0, behavior: 'smooth' }
  }
})

// Maps a backend role string to the URL prefix used across the dashboard
// routes above. Mirrors the same mapping used in Sidebar.vue / DashboardNavbar.vue
// — keep these in sync if you ever rename a role or a route prefix.
function getRolePrefix(role) {
  switch (role) {
    case 'Admin':
    case 'Administrator': return 'admin'
    case 'Officer': return 'officer'
    case 'Worker': return 'worker'
    case 'Citizen':
    default: return 'citizen'
  }
}

router.beforeEach((to, from, next) => {
  document.title = to.meta.title || 'CivicDesk'

  const token = localStorage.getItem('token')
  const isLoggedIn = !!token

  let user = null
  if (isLoggedIn) {
    try {
      user = JSON.parse(localStorage.getItem('user'))
    } catch (err) {
      // Corrupted/stale localStorage — treat as logged out rather than crash.
      user = null
    }
  }

  const rolePrefix = user ? getRolePrefix(user.role) : null

  // 1. Guest-only pages (Landing, Login, Register, Forgot Password):
  //    a logged-in user gets bounced straight to their own dashboard.
  if (to.meta.guestOnly && isLoggedIn && rolePrefix) {
    return next(`/${rolePrefix}/dashboard`)
  }

  // 2. Protected pages: no valid session -> send to Login, remembering
  //    where they were headed so Login.vue can send them back after auth.
  if (to.meta.requiresAuth && !isLoggedIn) {
    return next({ path: '/login', query: { redirect: to.fullPath } })
  }

  // 3. Protected pages: logged in, but the URL's role section doesn't match
  //    their actual role (e.g. a Citizen typing /officer/dashboard).
  //    Bounce them to their own dashboard instead of letting them in.
  if (to.meta.requiresAuth && isLoggedIn) {
    const sectionPrefix = to.path.split('/')[1]
    if (sectionPrefix !== rolePrefix) {
      return next(`/${rolePrefix}/dashboard`)
    }
  }

  next()
})

export default router