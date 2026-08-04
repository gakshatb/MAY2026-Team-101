import { createRouter, createWebHistory } from 'vue-router'

// --- Layout ---
import DashboardLayout from '../components/layouts/DashboardLayout.vue'

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
import ActivityView from '../views/citizen/Activity.vue'

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
import AdminNotifications from '../views/admin/Notifications.vue'
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

    // --- Citizen section ---
    {
      path: '/citizen',
      component: DashboardLayout,
      meta: { requiresAuth: true },
      children: [
        { path: 'dashboard', name: 'CitizenDashboard', component: Dashboard, meta: { title: 'Dashboard | CivicDesk', pageTitle: 'Dashboard' } },
        { path: 'profile', name: 'CitizenProfile', component: Profile, meta: { title: 'Profile | CivicDesk', pageTitle: 'Profile' } },
        { path: 'notifications', name: 'CitizenNotifications', component: Notifications, meta: { title: 'Notifications | CivicDesk', pageTitle: 'Notifications' } },
        { path: 'complaints', name: 'MyComplaints', component: MyComplaints, meta: { title: 'My Complaints | CivicDesk', pageTitle: 'My Complaints' } },
        { path: 'submit', name: 'SubmitComplaint', component: SubmitComplaint, meta: { title: 'Submit Complaint | CivicDesk', pageTitle: 'Submit Complaint' } },
        { path: 'complaintdetails/:id?', name: 'ComplaintDetails', component: ComplaintDetails, meta: { title: 'Details | CivicDesk', pageTitle: 'Complaint Details' }, props: true },
        { path: 'track/:id?', name: 'ComplaintTracking', component: ComplaintTracking, meta: { title: 'Track | CivicDesk', pageTitle: 'Complaint Tracking' }, props: true },
        { path: 'feedback/:id?', name: 'CitizenFeedback', component: Feedback, meta: { title: 'Feedback | CivicDesk', pageTitle: 'Complaint Feedback' }, props: true },
        { path: 'activity', name: 'CitizenActivity', component: ActivityView, meta: { title: 'Activity | CivicDesk', pageTitle: 'Account Activity' } },
      ]
    },

    // --- Officer section ---
    {
      path: '/officer',
      component: DashboardLayout,
      meta: { requiresAuth: true },
      children: [
        { path: 'dashboard', name: 'OfficerDashboard', component: OfficerDashboard, meta: { title: 'Officer Dashboard | CivicDesk', pageTitle: 'Dashboard' } },
        { path: 'complaints', name: 'OfficerComplaintManagement', component: ComplaintManagement, meta: { title: 'Complaint Management | CivicDesk', pageTitle: 'Complaint Management' } },
        { path: 'complaintdetails/:id', name: 'OfficerComplaintDetails', component: OfficerComplaintDetails, meta: { title: 'Complaint Details | CivicDesk', pageTitle: 'Complaint Details' }, props: true },
        { path: 'workers', name: 'ManageWorkers', component: ManageWorkers, meta: { title: 'Manage Workers | CivicDesk', pageTitle: 'Manage Workers' } },
        { path: 'assign/:id', name: 'AssignWorker', component: AssignWorker, meta: { title: 'Assign Worker | CivicDesk', pageTitle: 'Assign Worker' }, props: true },
        { path: 'analytics', name: 'AnalyticsReports', component: AnalyticsReports, meta: { title: 'Analytics | CivicDesk', pageTitle: 'Analytics & Reports' } },
        { path: 'notifications', name: 'OfficerNotifications', component: OfficerNotifications, meta: { title: 'Notifications | CivicDesk', pageTitle: 'Notifications' } },
        { path: 'profile', name: 'OfficerProfile', component: OfficerProfile, meta: { title: 'Profile | CivicDesk', pageTitle: 'Profile' } },
      ]
    },

    // --- Worker section ---
    {
      path: '/worker',
      component: DashboardLayout,
      meta: { requiresAuth: true },
      children: [
        { path: 'dashboard', name: 'WorkerDashboard', component: WorkerDashboard, meta: { title: 'Worker Dashboard | CivicDesk', pageTitle: 'Dashboard' } },
        { path: 'tasks', name: 'WorkerAssignedTasks', component: WorkerAssignedTasks, meta: { title: 'Assigned Tasks | CivicDesk', pageTitle: 'Assigned Tasks' } },
        { path: 'task/:id', name: 'WorkerTaskDetails', component: WorkerTaskDetails, meta: { title: 'Task Details | CivicDesk', pageTitle: 'Task Details' }, props: true },
        { path: 'update/:id', name: 'WorkerUpdateComplaint', component: WorkerUpdateComplaint, meta: { title: 'Update Complaint | CivicDesk', pageTitle: 'Update Complaint' }, props: true },
        { path: 'completed', name: 'WorkerCompletedTasks', component: WorkerCompletedTasks, meta: { title: 'Completed Tasks | CivicDesk', pageTitle: 'Completed Tasks' } },
        { path: 'notifications', name: 'WorkerNotifications', component: WorkerNotifications, meta: { title: 'Notifications | CivicDesk', pageTitle: 'Notifications' } },
        { path: 'profile', name: 'WorkerProfile', component: WorkerProfile, meta: { title: 'Profile | CivicDesk', pageTitle: 'Profile' } },
        { path: 'departmentapplications', name: 'DepartmentApplications', component: DepartmentApplications, meta: { title: 'Department Applications | CivicDesk', pageTitle: 'Department Applications' } },
      ]
    },

    // --- Admin section ---
    {
      path: '/admin',
      component: DashboardLayout,
      meta: { requiresAuth: true },
      children: [
        { path: 'dashboard', name: 'AdminDashboard', component: AdminDashboard, meta: { title: 'Admin Dashboard | CivicDesk', pageTitle: 'Dashboard' } },
        { path: 'departmentmanagement', name: 'DepartmentManagement', component: DepartmentManagement, meta: { title: 'Department Management | CivicDesk', pageTitle: 'Department Management' } },
        { path: 'officerdetails/:id?', name: 'OfficerDetails', component: OfficerDetails, meta: { title: 'Officer Details | CivicDesk', pageTitle: 'Officer Details' }, props: true },
        { path: 'notifications', name: 'AdminNotifications', component: AdminNotifications, meta: { title: 'Notifications | CivicDesk', pageTitle: 'Notifications' } },
        { path: 'officermanagement', name: 'OfficerManagement', component: OfficerManagement, meta: { title: 'Officer Management | CivicDesk', pageTitle: 'Officer Management' } },
        { path: 'profile', name: 'OfficersProfile', component: OfficersProfile, meta: { title: 'Profile | CivicDesk', pageTitle: 'Profile' } },
        { path: 'systemanalytics', name: 'SystemAnalytics', component: SystemAnalytics, meta: { title: 'System Analytics | CivicDesk', pageTitle: 'System Analytics' } },
        { path: 'activitylogs', name: 'ActivityLogs', component: ActivityLogs, meta: { title: 'Activity Logs | CivicDesk', pageTitle: 'Activity Logs' } },
        { path: 'announcements', name: 'Announcements', component: Announcements, meta: { title: 'Announcements | CivicDesk', pageTitle: 'Announcements' } },
      ]
    },

    // --- Fallback ---
    { path: '/:pathMatch(.*)*', redirect: '/' }
  ],
  scrollBehavior(to, from, savedPosition) {
    return savedPosition || { top: 0, behavior: 'smooth' }
  }
})

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
      user = null
    }
  }

  const rolePrefix = user ? getRolePrefix(user.role) : null

  if (to.meta.guestOnly && isLoggedIn && rolePrefix) {
    return next(`/${rolePrefix}/dashboard`)
  }

  if (to.meta.requiresAuth && !isLoggedIn) {
    return next({ path: '/login', query: { redirect: to.fullPath } })
  }

  if (to.meta.requiresAuth && isLoggedIn) {
    const sectionPrefix = to.path.split('/')[1]
    if (sectionPrefix !== rolePrefix) {
      return next(`/${rolePrefix}/dashboard`)
    }
  }

  next()
})

export default router