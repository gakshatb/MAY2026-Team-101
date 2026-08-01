<template>
      <main class="flex-1 overflow-x-hidden overflow-y-auto p-4 sm:p-6 lg:p-8">
        <div class="max-w-[1400px] mx-auto space-y-6">
          
          <!-- Breadcrumb & Header -->
          <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-4">
            <div>
              <nav class="flex text-sm text-slate-500 mb-2 font-medium">
                <router-link to="/officer/dashboard" class="hover:text-[#2563EB] transition-colors">Dashboard</router-link>
                <span class="mx-2">›</span>
                <router-link to="/officer/complaints" class="hover:text-[#2563EB] transition-colors">Complaint Management</router-link>
                <span class="mx-2">›</span>
                <span class="text-slate-900 font-semibold">{{ complaint.id }}</span>
              </nav>
              <div class="flex items-center gap-3 mt-1">
                <h1 class="text-2xl font-bold text-slate-900">{{ complaint.title }}</h1>
                <span :class="`px-2.5 py-1 text-xs font-bold rounded ${statusBadge(complaint.status)}`">{{ complaint.status }}</span>
              </div>
            </div>
            <div class="flex gap-3">
              <button class="p-2 bg-white border border-slate-200 text-slate-600 rounded-lg hover:bg-slate-50 transition-colors" title="Print Complaint">
                <Printer class="w-5 h-5" />
              </button>
              <button class="p-2 bg-white border border-slate-200 text-slate-600 rounded-lg hover:bg-slate-50 transition-colors" title="Download Report">
                <Download class="w-5 h-5" />
              </button>
            </div>
          </div>

          <!-- Quick Statistics Row -->
          <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div class="bg-white p-4 rounded-[14px] shadow-sm border border-slate-100 flex items-center gap-4">
              <div class="w-10 h-10 rounded-full bg-blue-50 text-[#2563EB] flex items-center justify-center shrink-0"><Clock class="w-5 h-5" /></div>
              <div>
                <p class="text-xs font-medium text-slate-500">Complaint Age</p>
                <p class="text-lg font-bold text-slate-900">{{ complaintAge }} Days</p>
              </div>
            </div>
            <div class="bg-white p-4 rounded-[14px] shadow-sm border border-slate-100 flex items-center gap-4">
              <div class="w-10 h-10 rounded-full bg-indigo-50 text-indigo-600 flex items-center justify-center shrink-0"><Calendar class="w-5 h-5" /></div>
              <div>
                <p class="text-xs font-medium text-slate-500">Resolution Target</p>
                <p class="text-lg font-bold text-slate-900">{{ complaint.targetDate }}</p>
              </div>
            </div>
            <div class="bg-white p-4 rounded-[14px] shadow-sm border border-slate-100 flex items-center gap-4">
              <div class="w-10 h-10 rounded-full bg-amber-50 text-amber-600 flex items-center justify-center shrink-0"><AlertCircle class="w-5 h-5" /></div>
              <div>
                <p class="text-xs font-medium text-slate-500">Days Remaining</p>
                <p class="text-lg font-bold text-amber-600">{{ daysRemaining }} Days</p>
              </div>
            </div>
            <div class="bg-white p-4 rounded-[14px] shadow-sm border border-slate-100 flex items-center gap-4">
              <div class="w-10 h-10 rounded-full flex items-center justify-center shrink-0" :class="priorityIconBg(complaint.priority)"><Flag class="w-5 h-5" /></div>
              <div>
                <p class="text-xs font-medium text-slate-500">Priority Level</p>
                <p class="text-lg font-bold" :class="priorityTextColor(complaint.priority)">{{ complaint.priority }}</p>
              </div>
            </div>
          </div>

          <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
            
            <!-- Left Column: Main Information -->
            <div class="lg:col-span-8 space-y-6">
              
              <!-- Complaint Description -->
              <div class="bg-white rounded-[14px] shadow-sm border border-slate-100 overflow-hidden">
                <div class="p-5 border-b border-slate-100 flex items-center gap-2">
                  <FileText class="w-5 h-5 text-slate-400" />
                  <h2 class="font-bold text-slate-900">Description & Details</h2>
                </div>
                <div class="p-5 space-y-4">
                  <p class="text-sm text-slate-700 leading-relaxed bg-slate-50 p-4 rounded-lg border border-slate-100">
                    {{ complaint.description }}
                  </p>
                  <div>
                    <h3 class="text-xs font-bold text-slate-500 uppercase tracking-wide mb-2">Complaint Tags</h3>
                    <div class="flex flex-wrap gap-2">
                      <span v-for="tag in complaint.tags" :key="tag" class="px-2.5 py-1 bg-blue-50 text-[#2563EB] text-xs font-semibold rounded-md">
                        {{ tag }}
                      </span>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Uploaded Images -->
              <div class="bg-white rounded-[14px] shadow-sm border border-slate-100 overflow-hidden">
                <div class="p-5 border-b border-slate-100 flex items-center gap-2">
                  <Image class="w-5 h-5 text-slate-400" />
                  <h2 class="font-bold text-slate-900">Evidence Attached ({{ complaint.images.length }})</h2>
                </div>
                <div class="p-5">
                  <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
                    <div 
                      v-for="(img, idx) in complaint.images" :key="idx" 
                      @click="openImage(img)"
                      class="aspect-square rounded-lg border border-slate-200 overflow-hidden cursor-pointer group relative"
                    >
                      <img :src="img" alt="Complaint Evidence" class="w-full h-full object-cover transition-transform duration-300 group-hover:scale-110" />
                      <div class="absolute inset-0 bg-slate-900/0 group-hover:bg-slate-900/20 transition-colors flex items-center justify-center">
                        <Eye class="w-6 h-6 text-white opacity-0 group-hover:opacity-100 transition-opacity" />
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Location Information -->
              <div class="bg-white rounded-[14px] shadow-sm border border-slate-100 overflow-hidden">
                <div class="p-5 border-b border-slate-100 flex items-center gap-2">
                  <MapPin class="w-5 h-5 text-slate-400" />
                  <h2 class="font-bold text-slate-900">Location Information</h2>
                </div>
                <div class="p-0 sm:flex">
                  <div class="p-5 flex-1 space-y-4">
                    <div>
                      <p class="text-xs font-medium text-slate-500">Address</p>
                      <p class="text-sm font-semibold text-slate-900 mt-0.5">{{ complaint.location.address }}</p>
                    </div>
                    <div class="grid grid-cols-2 gap-4">
                      <div>
                        <p class="text-xs font-medium text-slate-500">Ward Number</p>
                        <p class="text-sm font-semibold text-slate-900 mt-0.5">{{ complaint.location.ward }}</p>
                      </div>
                      <div>
                        <p class="text-xs font-medium text-slate-500">Area / Landmark</p>
                        <p class="text-sm font-semibold text-slate-900 mt-0.5">{{ complaint.location.area }}</p>
                      </div>
                    </div>
                    <div class="grid grid-cols-2 gap-4">
                      <div>
                        <p class="text-xs font-medium text-slate-500">Coordinates</p>
                        <p class="text-sm font-mono text-slate-600 mt-0.5">{{ complaint.location.lat }}, {{ complaint.location.lng }}</p>
                      </div>
                    </div>
                    <button class="w-full py-2 bg-slate-100 text-slate-700 text-sm font-bold rounded-lg hover:bg-slate-200 transition-colors flex items-center justify-center gap-2">
                      <Map class="w-4 h-4" /> Open in Maps
                    </button>
                  </div>
                  <div class="w-full sm:w-1/2 h-48 sm:h-auto bg-slate-100 flex items-center justify-center border-l border-slate-100">
                    <span class="text-slate-400 font-medium text-sm flex flex-col items-center gap-2">
                      <MapPin class="w-6 h-6" /> [ Map Placeholder ]
                    </span>
                  </div>
                </div>
              </div>

              <!-- Internal Notes Workspace -->
              <div class="bg-white rounded-[14px] shadow-sm border border-slate-100 overflow-hidden">
                <div class="p-5 border-b border-slate-100 flex justify-between items-center bg-amber-50/30">
                  <div class="flex items-center gap-2">
                    <Lock class="w-5 h-5 text-amber-500" />
                    <h2 class="font-bold text-slate-900">Internal Officer Notes</h2>
                  </div>
                  <span class="text-xs font-medium text-amber-600 bg-amber-100 px-2 py-0.5 rounded">Not visible to citizens</span>
                </div>
                <div class="p-5">
                  <div class="mb-4">
                    <textarea v-model="newNote" rows="3" placeholder="Add an internal note or observation..." class="w-full p-3 border border-slate-200 rounded-lg text-sm focus:ring-2 focus:ring-[#2563EB]/20 focus:border-[#2563EB] transition-all"></textarea>
                    <div class="flex justify-end mt-2">
                      <button @click="addNote" class="px-4 py-2 bg-[#2563EB] text-white text-sm font-medium rounded-lg hover:bg-[#1E40AF] transition-colors">Save Note</button>
                    </div>
                  </div>
                  
                  <div class="space-y-3">
                    <div v-for="note in internalNotes" :key="note.id" class="p-3 bg-slate-50 border border-slate-100 rounded-lg">
                      <div class="flex justify-between items-center mb-1">
                        <span class="text-xs font-bold text-slate-900">{{ note.author }}</span>
                        <span class="text-[10px] text-slate-500 font-medium">{{ note.timestamp }}</span>
                      </div>
                      <p class="text-sm text-slate-700">{{ note.text }}</p>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Assigned Worker & Resolution (Conditional) -->
              <div v-if="complaint.assignedWorker" class="bg-white rounded-[14px] shadow-sm border border-slate-100 overflow-hidden">
                 <div class="p-5 border-b border-slate-100 flex items-center gap-2">
                  <UserCheck class="w-5 h-5 text-slate-400" />
                  <h2 class="font-bold text-slate-900">Assignment & Resolution</h2>
                </div>
                <div class="p-5 grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div class="flex items-start gap-4">
                    <img :src="complaint.assignedWorker.avatar" class="w-12 h-12 rounded-full object-cover border border-slate-200" />
                    <div>
                      <p class="text-xs font-medium text-slate-500 mb-0.5">Assigned Field Worker</p>
                      <p class="font-bold text-slate-900">{{ complaint.assignedWorker.name }}</p>
                      <p class="text-sm text-slate-600">{{ complaint.assignedWorker.dept }}</p>
                      <div class="mt-2 flex gap-2">
                        <button class="px-2 py-1 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded text-xs font-medium transition-colors">View Profile</button>
                        <button class="px-2 py-1 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded text-xs font-medium transition-colors flex items-center gap-1"><Phone class="w-3 h-3"/> Call</button>
                      </div>
                    </div>
                  </div>
                  
                  <div v-if="complaint.status === 'Resolved' || complaint.status === 'Closed'" class="border-t md:border-t-0 md:border-l border-slate-100 pt-4 md:pt-0 md:pl-6">
                    <p class="text-xs font-medium text-slate-500 mb-2">Resolution Details</p>
                    <p class="text-sm text-slate-800 mb-1"><span class="font-semibold">Resolved On:</span> {{ complaint.resolution.date }}</p>
                    <p class="text-sm text-slate-800 mb-3"><span class="font-semibold">Time Taken:</span> {{ complaint.resolution.timeTaken }}</p>
                    <p class="text-xs font-semibold text-slate-600 mb-1">Worker Notes:</p>
                    <p class="text-sm text-slate-600 italic">"{{ complaint.resolution.notes }}"</p>
                  </div>
                </div>
              </div>

              <!-- Related Complaints Table -->
              <div class="bg-white rounded-[14px] shadow-sm border border-slate-100 overflow-hidden">
                <div class="p-5 border-b border-slate-100 flex items-center gap-2">
                  <Layers class="w-5 h-5 text-slate-400" />
                  <h2 class="font-bold text-slate-900">Recent Related Complaints (Same Area)</h2>
                </div>
                <div class="overflow-x-auto">
                  <table class="w-full text-left text-sm whitespace-nowrap">
                    <thead class="bg-slate-50 text-slate-500 font-medium">
                      <tr>
                        <th class="px-5 py-3">ID</th>
                        <th class="px-5 py-3">Category</th>
                        <th class="px-5 py-3">Status</th>
                        <th class="px-5 py-3">Date</th>
                        <th class="px-5 py-3"></th>
                      </tr>
                    </thead>
                    <tbody class="divide-y divide-slate-100">
                      <tr v-for="rel in relatedComplaints" :key="rel.id" class="hover:bg-slate-50">
                        <td class="px-5 py-3 font-mono font-medium text-slate-900">{{ rel.id }}</td>
                        <td class="px-5 py-3 text-slate-600">{{ rel.category }}</td>
                        <td class="px-5 py-3"><span :class="`px-2 py-0.5 rounded text-[10px] font-bold ${statusBadge(rel.status)}`">{{ rel.status }}</span></td>
                        <td class="px-5 py-3 text-slate-500">{{ rel.date }}</td>
                        <td class="px-5 py-3 text-right">
                          <button class="text-[#2563EB] font-medium text-xs hover:underline">View</button>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>

            </div>

            <!-- Right Column: Sidebar Actions & Context -->
            <div class="lg:col-span-4 space-y-6">
              
              <!-- Quick Actions Panel -->
              <div class="bg-white rounded-[14px] shadow-sm border border-[#2563EB]/20 overflow-hidden">
                <div class="p-4 bg-[#2563EB]/5 border-b border-[#2563EB]/10">
                  <h2 class="font-bold text-[#1E40AF]">Officer Actions</h2>
                </div>
                <div class="p-2 space-y-1">
                  <button @click="openModal('verify')" v-if="complaint.status === 'Submitted'" class="w-full px-4 py-2.5 flex items-center gap-3 text-sm font-medium text-slate-700 hover:bg-slate-50 rounded-lg transition-colors">
                    <ShieldCheck class="w-4 h-4 text-green-600" /> Verify Complaint
                  </button>
                  <button @click="openModal('assign')" class="w-full px-4 py-2.5 flex items-center gap-3 text-sm font-medium text-slate-700 hover:bg-slate-50 rounded-lg transition-colors">
                    <UserPlus class="w-4 h-4 text-purple-600" /> Assign Worker
                  </button>
                  <button @click="openModal('status')" class="w-full px-4 py-2.5 flex items-center gap-3 text-sm font-medium text-slate-700 hover:bg-slate-50 rounded-lg transition-colors">
                    <Activity class="w-4 h-4 text-blue-600" /> Update Status
                  </button>
                  <button @click="openModal('priority')" class="w-full px-4 py-2.5 flex items-center gap-3 text-sm font-medium text-slate-700 hover:bg-slate-50 rounded-lg transition-colors">
                    <Flag class="w-4 h-4 text-amber-600" /> Change Priority
                  </button>
                  <div class="h-px bg-slate-100 my-1 mx-4"></div>
                  <button class="w-full px-4 py-2.5 flex items-center gap-3 text-sm font-medium text-slate-700 hover:bg-slate-50 rounded-lg transition-colors">
                    <Mail class="w-4 h-4 text-slate-400" /> Request Info from Citizen
                  </button>
                  <button class="w-full px-4 py-2.5 flex items-center gap-3 text-sm font-medium text-red-600 hover:bg-red-50 rounded-lg transition-colors">
                    <XOctagon class="w-4 h-4" /> Close Complaint
                  </button>
                </div>
              </div>

              <!-- Citizen Context Card -->
              <div class="bg-white rounded-[14px] shadow-sm border border-slate-100 p-5">
                <div class="flex justify-between items-center mb-4">
                  <h2 class="font-bold text-slate-900 flex items-center gap-2"><User class="w-4 h-4 text-slate-400" /> Citizen Details</h2>
                </div>
                <div class="flex items-center gap-3 mb-4">
                  <img :src="citizen.avatar" class="w-10 h-10 rounded-full border border-slate-200" />
                  <div>
                    <p class="font-bold text-slate-900 text-sm">{{ citizen.name }}</p>
                    <p class="text-xs text-slate-500 font-mono">{{ citizen.id }}</p>
                  </div>
                </div>
                <div class="space-y-3 text-sm">
                  <div class="flex justify-between border-b border-slate-50 pb-2">
                    <span class="text-slate-500">Phone</span>
                    <span class="font-medium text-slate-900">{{ citizen.phone }}</span>
                  </div>
                  <div class="flex justify-between border-b border-slate-50 pb-2">
                    <span class="text-slate-500">Email</span>
                    <span class="font-medium text-slate-900 truncate max-w-[150px]">{{ citizen.email }}</span>
                  </div>
                  <div class="flex justify-between border-b border-slate-50 pb-2">
                    <span class="text-slate-500">Registered</span>
                    <span class="font-medium text-slate-900">{{ citizen.registered }}</span>
                  </div>
                  <div class="flex justify-between pb-1">
                    <span class="text-slate-500">Prior Complaints</span>
                    <span class="font-bold text-[#2563EB] cursor-pointer hover:underline">{{ citizen.prevComplaints }} Reports</span>
                  </div>
                </div>
                <div class="flex gap-2 mt-4">
                  <button class="flex-1 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-lg text-xs font-bold flex items-center justify-center gap-1 transition-colors"><Phone class="w-3 h-3"/> Call</button>
                  <button class="flex-1 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-lg text-xs font-bold flex items-center justify-center gap-1 transition-colors"><Mail class="w-3 h-3"/> Email</button>
                </div>
              </div>

              <!-- History / Timeline -->
              <div class="bg-white rounded-[14px] shadow-sm border border-slate-100 p-5">
                <h2 class="font-bold text-slate-900 flex items-center gap-2 mb-6"><History class="w-4 h-4 text-slate-400" /> Complete History</h2>
                <div class="relative pl-4 border-l-2 border-slate-100 space-y-6">
                  
                  <div v-for="(hist, idx) in complaintHistory" :key="idx" class="relative">
                    <div class="absolute -left-[21px] w-2.5 h-2.5 bg-slate-200 rounded-full ring-4 ring-white" :class="{'bg-[#2563EB]': idx === 0}"></div>
                    <p class="text-sm font-bold text-slate-900">{{ hist.action }}</p>
                    <div class="flex items-center gap-2 text-[11px] text-slate-500 mt-0.5 font-medium">
                      <span>{{ hist.date }} • {{ hist.time }}</span>
                      <span>|</span>
                      <span>By: {{ hist.user }}</span>
                    </div>
                    <p v-if="hist.detail" class="text-xs text-slate-600 mt-2 bg-slate-50 p-2 rounded border border-slate-100">{{ hist.detail }}</p>
                  </div>

                </div>
              </div>

            </div>
          </div>
        </div>
      </main>
    <!-- Modals (Teleported) -->
    <Teleport to="body">
      
      <!-- Image Viewer Modal -->
      <div v-if="previewImage" class="fixed inset-0 z-50 bg-slate-900/90 backdrop-blur-sm flex items-center justify-center p-4 animate-fade-in">
        <button @click="previewImage = null" class="absolute top-6 right-6 text-white hover:text-slate-300 p-2"><X class="w-8 h-8" /></button>
        <img :src="previewImage" class="max-w-full max-h-[90vh] object-contain rounded-lg shadow-2xl" />
        <a :href="previewImage" download="Evidence.jpg" class="absolute bottom-6 bg-white/10 hover:bg-white/20 text-white px-6 py-2.5 rounded-full backdrop-blur-md flex items-center gap-2 font-medium transition-colors">
          <Download class="w-4 h-4" /> Download Image
        </a>
      </div>

      <!-- Update Status Modal -->
      <div v-if="activeModal === 'status'" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/50 backdrop-blur-sm animate-fade-in">
        <div class="bg-white rounded-[14px] w-full max-w-sm shadow-2xl overflow-hidden">
          <div class="p-5 border-b border-slate-100 flex justify-between items-center">
            <h3 class="font-bold text-lg text-slate-900">Update Status</h3>
            <button @click="activeModal = null" class="text-slate-400 hover:text-slate-600"><X class="w-5 h-5"/></button>
          </div>
          <div class="p-5 space-y-4">
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-1.5">New Status</label>
              <select v-model="modalForms.status" class="w-full bg-slate-50 border border-slate-200 text-slate-900 text-sm rounded-lg focus:ring-[#2563EB] focus:border-[#2563EB] p-2.5">
                <option value="Submitted">Submitted</option>
                <option value="Verified">Verified</option>
                <option value="Assigned">Assigned</option>
                <option value="In Progress">In Progress</option>
                <option value="Resolved">Resolved</option>
                <option value="Closed">Closed</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-1.5">Officer Remarks</label>
              <textarea v-model="modalForms.remarks" rows="3" placeholder="Explain the reason for this status change..." class="w-full p-2.5 border border-slate-200 rounded-lg text-sm focus:ring-2 focus:ring-[#2563EB]/20 focus:border-[#2563EB]"></textarea>
            </div>
          </div>
          <div class="p-5 bg-slate-50 border-t border-slate-100 flex justify-end gap-3">
            <button @click="activeModal = null" class="px-4 py-2 text-sm font-medium text-slate-600 hover:bg-slate-200 rounded-lg">Cancel</button>
            <button @click="saveModal('status')" class="px-4 py-2 text-sm font-medium text-white bg-[#2563EB] hover:bg-[#1E40AF] rounded-lg shadow-sm">Update Status</button>
          </div>
        </div>
      </div>

      <!-- Priority Modal -->
      <div v-if="activeModal === 'priority'" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/50 backdrop-blur-sm animate-fade-in">
        <div class="bg-white rounded-[14px] w-full max-w-sm shadow-2xl overflow-hidden">
          <div class="p-5 border-b border-slate-100 flex justify-between items-center">
            <h3 class="font-bold text-lg text-slate-900">Change Priority</h3>
            <button @click="activeModal = null" class="text-slate-400 hover:text-slate-600"><X class="w-5 h-5"/></button>
          </div>
          <div class="p-5 space-y-3">
            <label v-for="pri in ['Emergency', 'High', 'Medium', 'Low']" :key="pri" class="flex items-center gap-3 p-3 border border-slate-100 rounded-lg cursor-pointer hover:bg-slate-50 transition-colors">
              <input type="radio" :value="pri" v-model="modalForms.priority" class="w-4 h-4 text-[#2563EB] focus:ring-[#2563EB] border-slate-300" />
              <span class="text-sm font-bold flex-1" :class="priorityTextColor(pri)">{{ pri }}</span>
              <span class="text-[10px] text-slate-500 uppercase font-bold" v-if="modalForms.priority === pri">Selected</span>
            </label>
          </div>
          <div class="p-5 bg-slate-50 border-t border-slate-100 flex justify-end gap-3">
            <button @click="activeModal = null" class="px-4 py-2 text-sm font-medium text-slate-600 hover:bg-slate-200 rounded-lg">Cancel</button>
            <button @click="saveModal('priority')" class="px-4 py-2 text-sm font-medium text-white bg-[#2563EB] hover:bg-[#1E40AF] rounded-lg shadow-sm">Save Priority</button>
          </div>
        </div>
      </div>

      <!-- Assign Worker Modal -->
      <div v-if="activeModal === 'assign'" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/50 backdrop-blur-sm animate-fade-in">
        <div class="bg-white rounded-[14px] w-full max-w-2xl shadow-2xl overflow-hidden flex flex-col max-h-[85vh]">
          <div class="p-5 border-b border-slate-100 flex justify-between items-center shrink-0">
            <div>
              <h3 class="font-bold text-lg text-slate-900">Assign Field Worker</h3>
              <p class="text-xs text-slate-500">Filter and select an appropriate worker for this task.</p>
            </div>
            <button @click="activeModal = null" class="text-slate-400 hover:text-slate-600"><X class="w-5 h-5"/></button>
          </div>
          
          <div class="p-4 bg-slate-50 border-b border-slate-100 shrink-0 flex gap-3">
            <div class="relative flex-1">
              <Search class="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
              <input type="text" placeholder="Search name or department..." class="w-full pl-9 pr-4 py-2 border border-slate-200 rounded-lg text-sm focus:ring-[#2563EB] focus:border-[#2563EB]" />
            </div>
            <select class="border border-slate-200 text-slate-700 text-sm rounded-lg focus:ring-[#2563EB] focus:border-[#2563EB] px-3 py-2 bg-white">
              <option>All Departments</option>
              <option>Roads & Infrastructure</option>
              <option>Sanitation</option>
            </select>
          </div>

          <div class="flex-1 overflow-y-auto p-2">
            <div class="overflow-x-auto">
              <table class="w-full text-left text-sm whitespace-nowrap">
                <thead class="text-slate-400 text-xs uppercase bg-white sticky top-0">
                  <tr>
                    <th class="px-4 py-2 font-semibold">Worker</th>
                    <th class="px-4 py-2 font-semibold">Current Tasks</th>
                    <th class="px-4 py-2 font-semibold">Experience</th>
                    <th class="px-4 py-2 font-semibold text-right">Action</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-slate-50">
                  <tr v-for="worker in dummyWorkers" :key="worker.id" class="hover:bg-slate-50 transition-colors">
                    <td class="px-4 py-3">
                      <div class="flex items-center gap-3">
                        <img :src="worker.avatar" class="w-8 h-8 rounded-full border border-slate-200 object-cover" />
                        <div>
                          <p class="font-bold text-slate-900 leading-none">{{ worker.name }}</p>
                          <p class="text-[11px] text-slate-500 mt-1">{{ worker.dept }}</p>
                        </div>
                      </div>
                    </td>
                    <td class="px-4 py-3">
                      <span class="px-2 py-1 rounded text-xs font-bold" :class="worker.tasks > 3 ? 'bg-amber-100 text-amber-700' : 'bg-green-100 text-green-700'">{{ worker.tasks }} Active</span>
                    </td>
                    <td class="px-4 py-3 text-slate-600">{{ worker.exp }} Yrs</td>
                    <td class="px-4 py-3 text-right">
                      <button @click="activeModal = null" class="px-3 py-1.5 bg-blue-50 text-[#2563EB] hover:bg-[#2563EB] hover:text-white text-xs font-bold rounded transition-colors">Assign</button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </Teleport>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import Sidebar from '@/components/dashboard/Sidebar.vue'
import DashboardNavbar from '@/components/dashboard/DashboardNavbar.vue'
import { 
  Printer, Download, Clock, Calendar, AlertCircle, Flag, FileText, Image, Eye,
  MapPin, Map, Lock, UserCheck, Phone, Layers, ShieldCheck, UserPlus, Activity,
  Mail, XOctagon, User, History, X, Search
} from 'lucide-vue-next'

// Layout State
const isSidebarOpen = ref(false)

// Modals State
const previewImage = ref(null)
const activeModal = ref(null)
const openImage = (url) => { previewImage.value = url }
const openModal = (type) => { activeModal.value = type }
const saveModal = (type) => { activeModal.value = null } // Mock save action

const modalForms = reactive({
  status: 'In Progress',
  remarks: '',
  priority: 'High'
})

const newNote = ref('')
const addNote = () => {
  if(!newNote.value.trim()) return
  internalNotes.unshift({
    id: Date.now(),
    author: 'Officer (You)',
    timestamp: 'Just now',
    text: newNote.value
  })
  newNote.value = ''
}

// Dummy Data
const complaint = reactive({
  id: 'CMP-2026-0892',
  title: 'Deep Pothole causing traffic disruption',
  category: 'Roads & Infra',
  priority: 'High',
  status: 'In Progress',
  description: 'There is a massive pothole that formed after the recent rains. It is causing severe traffic slowdowns during peak hours and is highly dangerous for two-wheelers at night. Multiple vehicles have already been damaged.',
  tags: ['Road Damage', 'Traffic Hazard', 'Urgent'],
  submittedDate: 'Jul 05, 2026',
  targetDate: 'Jul 12, 2026',
  images: [
    'https://images.unsplash.com/photo-1515162816999-a0c47dc192f7?auto=format&fit=crop&q=80&w=400',
    'https://images.unsplash.com/photo-1584985614946-bdeeb2bc4db1?auto=format&fit=crop&q=80&w=400'
  ],
  location: {
    address: 'Opposite City Center Mall, Main Gate',
    ward: 'Ward 14',
    area: 'Downtown',
    lat: '18.5204',
    lng: '73.8567'
  },
  assignedWorker: {
    name: 'Amit Singh',
    dept: 'Roads Department',
    avatar: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&q=80&w=200'
  }
})

const citizen = {
  name: 'Rahul Verma',
  id: 'CTZ-9021',
  phone: '+91 98765 43210',
  email: 'rahul.v@example.com',
  registered: 'Jan 15, 2025',
  prevComplaints: 3,
  avatar: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?auto=format&fit=crop&q=80&w=200'
}

const internalNotes = reactive([
  { id: 1, author: 'Chief Officer S. Patel', timestamp: 'Jul 07, 2026 • 10:15 AM', text: 'Verified the issue via traffic camera. Escalated priority to High due to accident risk.' },
  { id: 2, author: 'System Admin', timestamp: 'Jul 05, 2026 • 09:00 AM', text: 'Complaint routed to Roads Dept.' }
])

const complaintHistory = [
  { action: 'Status changed to In Progress', date: 'Jul 08, 2026', time: '14:30', user: 'Amit Singh (Worker)', detail: 'Worker started patching work on site.' },
  { action: 'Worker Assigned', date: 'Jul 07, 2026', time: '11:00', user: 'S. Patel (Officer)', detail: 'Assigned to Amit Singh.' },
  { action: 'Priority changed to High', date: 'Jul 07, 2026', time: '10:15', user: 'S. Patel (Officer)', detail: null },
  { action: 'Complaint Verified', date: 'Jul 07, 2026', time: '10:10', user: 'S. Patel (Officer)', detail: null },
  { action: 'Complaint Submitted', date: 'Jul 05, 2026', time: '08:45', user: 'Rahul Verma (Citizen)', detail: 'Submitted via Mobile App' },
]

const relatedComplaints = [
  { id: 'CMP-0870', category: 'Streetlight', status: 'Pending', date: 'Jul 04' },
  { id: 'CMP-0841', category: 'Road Damage', status: 'Resolved', date: 'Jun 28' },
]

const dummyWorkers = [
  { id: 1, name: 'Amit Singh', dept: 'Roads Dept', tasks: 2, exp: 5, avatar: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&q=80&w=100' },
  { id: 2, name: 'Suresh Patil', dept: 'Roads Dept', tasks: 4, exp: 8, avatar: 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&q=80&w=100' },
  { id: 3, name: 'Vijay Sharma', dept: 'Sanitation', tasks: 1, exp: 3, avatar: 'https://images.unsplash.com/photo-1599566150163-29194dcaad36?auto=format&fit=crop&q=80&w=100' },
]

// Computed Stats
const complaintAge = computed(() => 4) // Mocked for Jul 5 to Jul 9
const daysRemaining = computed(() => 3) // Mocked for target Jul 12

// Helper methods
const statusBadge = (status) => {
  const map = {
    'Submitted': 'bg-slate-100 text-slate-700',
    'Verified': 'bg-blue-100 text-blue-700',
    'Assigned': 'bg-purple-100 text-purple-700',
    'In Progress': 'bg-amber-100 text-amber-700',
    'Resolved': 'bg-green-100 text-green-700',
    'Pending': 'bg-amber-100 text-amber-700'
  }
  return map[status] || 'bg-slate-100 text-slate-700'
}

const priorityTextColor = (priority) => {
  const map = {
    'Emergency': 'text-red-600',
    'High': 'text-orange-600',
    'Medium': 'text-blue-600',
    'Low': 'text-slate-600'
  }
  return map[priority]
}

const priorityIconBg = (priority) => {
  const map = {
    'Emergency': 'bg-red-50 text-red-600',
    'High': 'bg-orange-50 text-orange-600',
    'Medium': 'bg-blue-50 text-blue-600',
    'Low': 'bg-slate-100 text-slate-600'
  }
  return map[priority]
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

.font-sans {
  font-family: 'Inter', sans-serif;
}

.animate-fade-in {
  animation: fadeIn 0.2s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

/* Custom Scrollbar for Drawer & Main Area */
::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}
::-webkit-scrollbar-track {
  background: transparent;
}
::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 10px;
}
::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}
</style>