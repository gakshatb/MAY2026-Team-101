<template>
      <main class="flex-1 overflow-x-hidden overflow-y-auto p-4 sm:p-6 lg:p-8">
        <div v-if="isLoading" class="max-w-[1400px] mx-auto py-24 text-center text-slate-400">Loading complaint…</div>
        <div v-else-if="loadError" class="max-w-[1400px] mx-auto py-24 text-center text-red-500">{{ loadError }}</div>
        <div v-else class="max-w-[1400px] mx-auto space-y-6">
          
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
          </div>

          <!-- Quick Statistics Row -->
          <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div class="bg-white p-4 rounded-[14px] shadow-sm border border-slate-100 flex items-center gap-4">
              <div class="w-10 h-10 rounded-full bg-blue-50 text-[#2563EB] flex items-center justify-center shrink-0"><Clock class="w-5 h-5" /></div>
              <div>
                <p class="text-xs font-medium text-slate-500">Complaint Age</p>
                <p class="text-lg font-bold text-slate-900">{{ complaint.complaintAge }} Days</p>
              </div>
            </div>
            <div class="bg-white p-4 rounded-[14px] shadow-sm border border-slate-100 flex items-center gap-4">
              <div class="w-10 h-10 rounded-full bg-indigo-50 text-indigo-600 flex items-center justify-center shrink-0"><Calendar class="w-5 h-5" /></div>
              <div>
                <p class="text-xs font-medium text-slate-500">Target Date (7-day SLA)</p>
                <p class="text-lg font-bold text-slate-900">{{ complaint.targetDate }}</p>
              </div>
            </div>
            <div class="bg-white p-4 rounded-[14px] shadow-sm border border-slate-100 flex items-center gap-4">
              <div class="w-10 h-10 rounded-full bg-amber-50 text-amber-600 flex items-center justify-center shrink-0"><AlertCircle class="w-5 h-5" /></div>
              <div>
                <p class="text-xs font-medium text-slate-500">Days Remaining</p>
                <p class="text-lg font-bold text-amber-600">{{ complaint.daysRemaining }} Days</p>
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
                <div class="p-5">
                  <p class="text-sm text-slate-700 leading-relaxed bg-slate-50 p-4 rounded-lg border border-slate-100">
                    {{ complaint.description }}
                  </p>
                </div>
              </div>

              <!-- Uploaded Images -->
              <div class="bg-white rounded-[14px] shadow-sm border border-slate-100 overflow-hidden">
                <div class="p-5 border-b border-slate-100 flex items-center gap-2">
                  <Image class="w-5 h-5 text-slate-400" />
                  <h2 class="font-bold text-slate-900">Evidence Attached ({{ complaint.images.length }})</h2>
                </div>
                <div class="p-5">
                  <div v-if="complaint.images.length" class="grid grid-cols-2 sm:grid-cols-4 gap-4">
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
                  <p v-else class="text-sm text-slate-400">No images were attached to this complaint.</p>
                </div>
              </div>

              <!-- Location Information -->
              <div class="bg-white rounded-[14px] shadow-sm border border-slate-100 overflow-hidden">
                <div class="p-5 border-b border-slate-100 flex items-center gap-2">
                  <MapPin class="w-5 h-5 text-slate-400" />
                  <h2 class="font-bold text-slate-900">Location Information</h2>
                </div>
                <div class="p-5 space-y-4">
                  <div>
                    <p class="text-xs font-medium text-slate-500">Address</p>
                    <p class="text-sm font-semibold text-slate-900 mt-0.5">{{ complaint.location.address }}</p>
                  </div>
                  <div class="grid grid-cols-2 gap-4">
                    <div>
                      <p class="text-xs font-medium text-slate-500">Ward</p>
                      <p class="text-sm font-semibold text-slate-900 mt-0.5">{{ complaint.location.ward }}</p>
                    </div>
                    <div>
                      <p class="text-xs font-medium text-slate-500">Area</p>
                      <p class="text-sm font-semibold text-slate-900 mt-0.5">{{ complaint.location.area }}</p>
                    </div>
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
                  <span class="text-xs font-medium text-slate-500">Private — never shown to citizen or worker</span>
                </div>
                <div class="p-5">
                  <div class="mb-4">
                    <textarea v-model="newNote" rows="3" placeholder="Add an internal note or observation..." class="w-full p-3 border border-slate-200 rounded-lg text-sm focus:ring-2 focus:ring-[#2563EB]/20 focus:border-[#2563EB] transition-all"></textarea>
                    <div class="flex justify-end mt-2">
                      <button @click="addNote" :disabled="isSavingNote || !newNote.trim()" class="px-4 py-2 bg-[#2563EB] text-white text-sm font-medium rounded-lg hover:bg-[#1E40AF] transition-colors disabled:opacity-50 disabled:cursor-not-allowed">
                        {{ isSavingNote ? 'Saving…' : 'Save Note' }}
                      </button>
                    </div>
                  </div>
                  <div class="space-y-3">
                    <div v-for="note in internalNotes" :key="note.id" class="p-3 bg-slate-50 border border-slate-100 rounded-lg group">
                      <div class="flex justify-between items-center mb-1">
                        <span class="text-xs font-bold text-slate-900">{{ note.author }}</span>
                        <div class="flex items-center gap-2">
                          <span class="text-[10px] text-slate-500 font-medium">{{ note.timestamp }}</span>
                          <button @click="deleteNote(note.id)" class="opacity-0 group-hover:opacity-100 transition-opacity text-slate-400 hover:text-red-500" title="Delete note">
                            <X class="w-3.5 h-3.5" />
                          </button>
                        </div>
                      </div>
                      <p class="text-sm text-slate-700">{{ note.text }}</p>
                    </div>
                    <p v-if="internalNotes.length === 0" class="text-sm text-slate-400">No notes yet.</p>
                  </div>
                </div>
              </div>

              <!-- Assigned Worker & Resolution -->
              <div v-if="complaint.worker" class="bg-white rounded-[14px] shadow-sm border border-slate-100 overflow-hidden">
                 <div class="p-5 border-b border-slate-100 flex items-center gap-2">
                  <UserCheck class="w-5 h-5 text-slate-400" />
                  <h2 class="font-bold text-slate-900">Assignment & Resolution</h2>
                </div>
                <div class="p-5 grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <p class="text-xs font-medium text-slate-500 mb-0.5">Assigned Field Worker</p>
                    <p class="font-bold text-slate-900">{{ complaint.worker }}</p>
                  </div>
                  <div v-if="complaint.resolution" class="border-t md:border-t-0 md:border-l border-slate-100 pt-4 md:pt-0 md:pl-6">
                    <p class="text-xs font-medium text-slate-500 mb-2">Resolution Details</p>
                    <p class="text-sm text-slate-800 mb-1"><span class="font-semibold">Resolved On:</span> {{ complaint.resolution.date }}</p>
                    <p class="text-sm text-slate-800 mb-3"><span class="font-semibold">Time Taken:</span> {{ complaint.resolution.timeTaken }}</p>
                    <p v-if="complaint.resolution.notes" class="text-xs font-semibold text-slate-600 mb-1">Officer Remarks:</p>
                    <p v-if="complaint.resolution.notes" class="text-sm text-slate-600 italic">"{{ complaint.resolution.notes }}"</p>
                  </div>
                </div>
              </div>

              <!-- Related Complaints Table -->
              <div v-if="complaint.relatedComplaints.length" class="bg-white rounded-[14px] shadow-sm border border-slate-100 overflow-hidden">
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
                      </tr>
                    </thead>
                    <tbody class="divide-y divide-slate-100">
                      <tr v-for="rel in complaint.relatedComplaints" :key="rel.id" class="hover:bg-slate-50">
                        <td class="px-5 py-3 font-mono font-medium text-slate-900">{{ rel.id }}</td>
                        <td class="px-5 py-3 text-slate-600">{{ rel.category }}</td>
                        <td class="px-5 py-3"><span :class="`px-2 py-0.5 rounded text-[10px] font-bold ${statusBadge(rel.status)}`">{{ rel.status }}</span></td>
                        <td class="px-5 py-3 text-slate-500">{{ rel.date }}</td>
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
                  <button @click="openModal('assign')" v-if="!complaint.worker && !['Resolved','Closed'].includes(complaint.status)" class="w-full px-4 py-2.5 flex items-center gap-3 text-sm font-medium text-slate-700 hover:bg-slate-50 rounded-lg transition-colors">
                    <UserPlus class="w-4 h-4 text-purple-600" /> Assign Worker
                  </button>
                  <button @click="openModal('status')" v-if="!['Resolved','Closed'].includes(complaint.status)" class="w-full px-4 py-2.5 flex items-center gap-3 text-sm font-medium text-slate-700 hover:bg-slate-50 rounded-lg transition-colors">
                    <Activity class="w-4 h-4 text-blue-600" /> Update Status
                  </button>
                  <button @click="openModal('priority')" v-if="!['Resolved','Closed'].includes(complaint.status)" class="w-full px-4 py-2.5 flex items-center gap-3 text-sm font-medium text-slate-700 hover:bg-slate-50 rounded-lg transition-colors">
                    <Flag class="w-4 h-4 text-amber-600" /> Change Priority
                  </button>
                  <div class="h-px bg-slate-100 my-1 mx-4" v-if="complaint.status === 'Assigned' && !complaint.worker"></div>
                  <button @click="openModal('return')" v-if="complaint.status === 'Assigned' && !complaint.worker" class="w-full px-4 py-2.5 flex items-center gap-3 text-sm font-medium text-amber-700 hover:bg-amber-50 rounded-lg transition-colors">
                    <Undo2 class="w-4 h-4" /> Send Back to Admin
                  </button>
                </div>
              </div>

              <!-- Citizen Context Card -->
              <div v-if="complaint.citizenDetails" class="bg-white rounded-[14px] shadow-sm border border-slate-100 p-5">
                <div class="flex justify-between items-center mb-4">
                  <h2 class="font-bold text-slate-900 flex items-center gap-2"><User class="w-4 h-4 text-slate-400" /> Citizen Details</h2>
                </div>
                <div class="mb-4">
                  <p class="font-bold text-slate-900 text-sm">{{ complaint.citizenDetails.name }}</p>
                </div>
                <div class="space-y-3 text-sm">
                  <div class="flex justify-between border-b border-slate-50 pb-2">
                    <span class="text-slate-500">Phone</span>
                    <span class="font-medium text-slate-900">{{ complaint.citizenDetails.phone || '—' }}</span>
                  </div>
                  <div class="flex justify-between border-b border-slate-50 pb-2">
                    <span class="text-slate-500">Email</span>
                    <span class="font-medium text-slate-900 truncate max-w-[150px]">{{ complaint.citizenDetails.email || '—' }}</span>
                  </div>
                  <div class="flex justify-between border-b border-slate-50 pb-2">
                    <span class="text-slate-500">Registered</span>
                    <span class="font-medium text-slate-900">{{ complaint.citizenDetails.registered }}</span>
                  </div>
                  <div class="flex justify-between pb-1">
                    <span class="text-slate-500">Prior Complaints</span>
                    <span class="font-bold text-[#2563EB]">{{ complaint.citizenDetails.prevComplaints }} Reports</span>
                  </div>
                </div>
              </div>

              <!-- History / Timeline -->
              <div class="bg-white rounded-[14px] shadow-sm border border-slate-100 p-5">
                <h2 class="font-bold text-slate-900 flex items-center gap-2 mb-6"><History class="w-4 h-4 text-slate-400" /> Complete History</h2>
                <div class="relative pl-4 border-l-2 border-slate-100 space-y-6">
                  <div v-for="(hist, idx) in complaint.history" :key="idx" class="relative">
                    <div class="absolute -left-[21px] w-2.5 h-2.5 bg-slate-200 rounded-full ring-4 ring-white" :class="{'bg-[#2563EB]': idx === 0}"></div>
                    <p class="text-sm font-bold text-slate-900">{{ hist.action }}</p>
                    <div class="flex items-center gap-2 text-[11px] text-slate-500 mt-0.5 font-medium">
                      <span>{{ hist.date }} • {{ hist.time }}</span>
                    </div>
                    <p v-if="hist.detail" class="text-xs text-slate-600 mt-2 bg-slate-50 p-2 rounded border border-slate-100">{{ hist.detail }}</p>
                  </div>
                  <p v-if="complaint.history.length === 0" class="text-sm text-slate-400">No history yet.</p>
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
      </div>

      <!-- Update Status Modal -->
      <div v-if="activeModal === 'status'" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/50 backdrop-blur-sm animate-fade-in">
        <div class="bg-white rounded-[14px] w-full max-w-sm shadow-2xl overflow-hidden">
          <div class="p-5 border-b border-slate-100 flex justify-between items-center">
            <h3 class="font-bold text-lg text-slate-900">Update Status</h3>
            <button @click="closeModal" class="text-slate-400 hover:text-slate-600"><X class="w-5 h-5"/></button>
          </div>
          <div class="p-5 space-y-4">
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-1.5">New Status</label>
              <select v-model="statusForm.status" class="w-full bg-slate-50 border border-slate-200 text-slate-900 text-sm rounded-lg focus:ring-[#2563EB] focus:border-[#2563EB] p-2.5">
                <option value="Assigned">Assigned</option>
                <option value="In Progress">In Progress</option>
              </select>
              <p class="text-xs text-slate-400 mt-1">Resolved is set by the field worker; Closed is set by admin.</p>
            </div>
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-1.5">Officer Remarks</label>
              <textarea v-model="statusForm.remark" rows="3" placeholder="Explain the reason for this status change..." class="w-full p-2.5 border border-slate-200 rounded-lg text-sm focus:ring-2 focus:ring-[#2563EB]/20 focus:border-[#2563EB]"></textarea>
            </div>
          </div>
          <div class="p-5 bg-slate-50 border-t border-slate-100 flex justify-end gap-3">
            <button @click="closeModal" class="px-4 py-2 text-sm font-medium text-slate-600 hover:bg-slate-200 rounded-lg">Cancel</button>
            <button @click="saveStatus" :disabled="isSaving" class="px-4 py-2 text-sm font-medium text-white bg-[#2563EB] hover:bg-[#1E40AF] rounded-lg shadow-sm disabled:opacity-50">Update Status</button>
          </div>
          <p v-if="modalError" class="text-red-600 text-xs px-5 pb-4">{{ modalError }}</p>
        </div>
      </div>

      <!-- Priority Modal -->
      <div v-if="activeModal === 'priority'" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/50 backdrop-blur-sm animate-fade-in">
        <div class="bg-white rounded-[14px] w-full max-w-sm shadow-2xl overflow-hidden">
          <div class="p-5 border-b border-slate-100 flex justify-between items-center">
            <h3 class="font-bold text-lg text-slate-900">Change Priority</h3>
            <button @click="closeModal" class="text-slate-400 hover:text-slate-600"><X class="w-5 h-5"/></button>
          </div>
          <div class="p-5 space-y-3">
            <label v-for="pri in ['Emergency', 'High', 'Medium', 'Low']" :key="pri" class="flex items-center gap-3 p-3 border border-slate-100 rounded-lg cursor-pointer hover:bg-slate-50 transition-colors">
              <input type="radio" :value="pri" v-model="priorityForm" class="w-4 h-4 text-[#2563EB] focus:ring-[#2563EB] border-slate-300" />
              <span class="text-sm font-bold flex-1" :class="priorityTextColor(pri)">{{ pri }}</span>
              <span class="text-[10px] text-slate-500 uppercase font-bold" v-if="priorityForm === pri">Selected</span>
            </label>
          </div>
          <div class="p-5 bg-slate-50 border-t border-slate-100 flex justify-end gap-3">
            <button @click="closeModal" class="px-4 py-2 text-sm font-medium text-slate-600 hover:bg-slate-200 rounded-lg">Cancel</button>
            <button @click="savePriority" :disabled="isSaving" class="px-4 py-2 text-sm font-medium text-white bg-[#2563EB] hover:bg-[#1E40AF] rounded-lg shadow-sm disabled:opacity-50">Save Priority</button>
          </div>
          <p v-if="modalError" class="text-red-600 text-xs px-5 pb-4">{{ modalError }}</p>
        </div>
      </div>

      <!-- Assign Worker Modal -->
      <div v-if="activeModal === 'assign'" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/50 backdrop-blur-sm animate-fade-in">
        <div class="bg-white rounded-[14px] w-full max-w-2xl shadow-2xl overflow-hidden flex flex-col max-h-[85vh]">
          <div class="p-5 border-b border-slate-100 flex justify-between items-center shrink-0">
            <div>
              <h3 class="font-bold text-lg text-slate-900">Assign Field Worker</h3>
              <p class="text-xs text-slate-500">Workers in your department.</p>
            </div>
            <button @click="closeModal" class="text-slate-400 hover:text-slate-600"><X class="w-5 h-5"/></button>
          </div>
          
          <div class="p-4 bg-slate-50 border-b border-slate-100 shrink-0">
            <div class="relative">
              <Search class="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
              <input v-model="workerSearch" type="text" placeholder="Search name..." class="w-full pl-9 pr-4 py-2 border border-slate-200 rounded-lg text-sm focus:ring-[#2563EB] focus:border-[#2563EB]" />
            </div>
          </div>

          <div class="flex-1 overflow-y-auto p-2">
            <p v-if="workersLoading" class="text-sm text-slate-400 text-center py-6">Loading workers…</p>
            <p v-else-if="filteredWorkers.length === 0" class="text-sm text-slate-400 text-center py-6">No workers found.</p>
            <table v-else class="w-full text-left text-sm whitespace-nowrap">
              <thead class="text-slate-400 text-xs uppercase bg-white sticky top-0">
                <tr>
                  <th class="px-4 py-2 font-semibold">Worker</th>
                  <th class="px-4 py-2 font-semibold">Current Tasks</th>
                  <th class="px-4 py-2 font-semibold text-right">Action</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-50">
                <tr v-for="worker in filteredWorkers" :key="worker.id" class="hover:bg-slate-50 transition-colors">
                  <td class="px-4 py-3">
                    <p class="font-bold text-slate-900 leading-none">{{ worker.name }}</p>
                  </td>
                  <td class="px-4 py-3">
                    <span class="px-2 py-1 rounded text-xs font-bold" :class="worker.activeTasks > 3 ? 'bg-amber-100 text-amber-700' : 'bg-green-100 text-green-700'">{{ worker.activeTasks }} Active</span>
                  </td>
                  <td class="px-4 py-3 text-right">
                    <button @click="assignWorker(worker.id)" :disabled="isSaving" class="px-3 py-1.5 bg-blue-50 text-[#2563EB] hover:bg-[#2563EB] hover:text-white text-xs font-bold rounded transition-colors disabled:opacity-50">Assign</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <p v-if="modalError" class="text-red-600 text-xs px-5 pb-4">{{ modalError }}</p>
        </div>
      </div>

      <!-- Return to Admin Modal -->
      <div v-if="activeModal === 'return'" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/50 backdrop-blur-sm animate-fade-in">
        <div class="bg-white rounded-[14px] w-full max-w-md shadow-2xl overflow-hidden">
          <div class="p-5 border-b border-slate-100 flex justify-between items-center">
            <h3 class="font-bold text-lg text-slate-900">Send Back to Admin</h3>
            <button @click="closeModal" class="text-slate-400 hover:text-slate-600"><X class="w-5 h-5"/></button>
          </div>
          <div class="p-5 space-y-4">
            <p class="text-sm text-slate-600">This unassigns the complaint from you and returns it to the admin queue for re-review.</p>
            <textarea v-model="returnRemark" rows="3" placeholder="Explain why this is being sent back (required)..." class="w-full p-2.5 border border-slate-200 rounded-lg text-sm focus:ring-2 focus:ring-[#2563EB]/20 focus:border-[#2563EB]"></textarea>
          </div>
          <div class="p-5 bg-slate-50 border-t border-slate-100 flex justify-end gap-3">
            <button @click="closeModal" class="px-4 py-2 text-sm font-medium text-slate-600 hover:bg-slate-200 rounded-lg">Cancel</button>
            <button @click="returnToAdmin" :disabled="!returnRemark.trim() || isSaving" class="px-4 py-2 text-sm font-medium text-white bg-amber-600 hover:bg-amber-700 rounded-lg shadow-sm disabled:opacity-50">Send Back</button>
          </div>
          <p v-if="modalError" class="text-red-600 text-xs px-5 pb-4">{{ modalError }}</p>
        </div>
      </div>
    </Teleport>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import Sidebar from '@/components/dashboard/Sidebar.vue'
import DashboardNavbar from '@/components/dashboard/DashboardNavbar.vue'
import { 
  Clock, Calendar, AlertCircle, Flag, FileText, Image, Eye,
  MapPin, Lock, UserCheck, Layers, UserPlus, Activity,
  User, History, X, Search, Undo2
} from 'lucide-vue-next'

const API_BASE = 'http://127.0.0.1:5000/api/officer'
const authHeaders = () => ({ headers: { Authorization: `Bearer ${localStorage.getItem('token')}` } })

const route = useRoute()
const router = useRouter()

// Layout State
const isSidebarOpen = ref(false)

// Complaint state
const complaint = ref({
  id: '', title: '', status: '', priority: '', description: '', images: [],
  location: { address: '', ward: '', area: '' }, worker: null, resolution: null,
  history: [], relatedComplaints: [], citizenDetails: null, complaintAge: 0,
  targetDate: '', daysRemaining: 0,
})
const isLoading = ref(true)
const loadError = ref('')

const fetchComplaint = async () => {
  isLoading.value = true
  loadError.value = ''
  try {
    let id = route.params.id
    if (!id) {
      const { data: listData } = await axios.get(`${API_BASE}/complaints`, { ...authHeaders(), params: { status: 'All' } })
      const openRows = (listData.complaints || []).filter(c => c.status === 'Assigned' || c.status === 'In Progress')
      const target = openRows[openRows.length - 1]
      if (!target) {
        loadError.value = 'You have no complaints to show yet.'
        isLoading.value = false
        return
      }
      id = target.rawId
      await router.replace(`/officer/complaintdetails/${id}`)
    }
    const { data } = await axios.get(`${API_BASE}/complaints/${id}`, authHeaders())
    complaint.value = data.complaint
  } catch (err) {
    loadError.value = err.response?.data?.message || 'Failed to load this complaint.'
  } finally {
    isLoading.value = false
  }
}
onMounted(fetchComplaint)

// Modals State
const previewImage = ref(null)
const activeModal = ref(null)
const modalError = ref('')
const isSaving = ref(false)
const openImage = (url) => { previewImage.value = url }
const openModal = (type) => {
  activeModal.value = type
  modalError.value = ''
  if (type === 'status') { statusForm.status = complaint.value.status === 'Assigned' ? 'In Progress' : complaint.value.status; statusForm.remark = '' }
  if (type === 'priority') priorityForm.value = complaint.value.priority
  if (type === 'return') returnRemark.value = ''
  if (type === 'assign') { workerSearch.value = ''; fetchWorkers() }
}
const closeModal = () => { activeModal.value = null }

const statusForm = reactive({ status: 'In Progress', remark: '' })
const priorityForm = ref('Medium')
const returnRemark = ref('')

const saveStatus = async () => {
  isSaving.value = true
  modalError.value = ''
  try {
    await axios.patch(`${API_BASE}/complaints/${route.params.id}/status`,
      { status: statusForm.status, remark: statusForm.remark }, authHeaders())
    closeModal()
    await fetchComplaint()
  } catch (err) {
    modalError.value = err.response?.data?.message || 'Failed to update status.'
  } finally {
    isSaving.value = false
  }
}

const savePriority = async () => {
  isSaving.value = true
  modalError.value = ''
  try {
    await axios.patch(`${API_BASE}/complaints/${route.params.id}/priority`,
      { priority: priorityForm.value }, authHeaders())
    closeModal()
    await fetchComplaint()
  } catch (err) {
    modalError.value = err.response?.data?.message || 'Failed to update priority.'
  } finally {
    isSaving.value = false
  }
}

const returnToAdmin = async () => {
  if (!returnRemark.value.trim()) return
  isSaving.value = true
  modalError.value = ''
  try {
    await axios.patch(`${API_BASE}/complaints/${route.params.id}/return-to-admin`,
      { remark: returnRemark.value }, authHeaders())
    router.push('/officer/complaints')
  } catch (err) {
    modalError.value = err.response?.data?.message || 'Failed to send complaint back.'
    isSaving.value = false
  }
}

// Workers (Assign modal)
const workers = ref([])
const workersLoading = ref(false)
const workerSearch = ref('')
const filteredWorkers = computed(() => {
  if (!workerSearch.value) return workers.value
  const q = workerSearch.value.toLowerCase()
  return workers.value.filter(w => w.name.toLowerCase().includes(q))
})
const fetchWorkers = async () => {
  workersLoading.value = true
  try {
    const { data } = await axios.get(`${API_BASE}/workers`, authHeaders())
    workers.value = data.workers
  } catch (err) {
    modalError.value = err.response?.data?.message || 'Failed to load workers.'
  } finally {
    workersLoading.value = false
  }
}
const assignWorker = async (workerId) => {
  isSaving.value = true
  modalError.value = ''
  try {
    await axios.patch(`${API_BASE}/complaints/${route.params.id}/assign-worker`,
      { worker_id: workerId }, authHeaders())
    closeModal()
    await fetchComplaint()
  } catch (err) {
    modalError.value = err.response?.data?.message || 'Failed to assign worker.'
  } finally {
    isSaving.value = false
  }
}

// Internal officer notes — persisted via /complaints/<id>/notes
const newNote = ref('')
const internalNotes = computed(() => complaint.value.officerNotes || [])
const isSavingNote = ref(false)
const addNote = async () => {
  if (!newNote.value.trim() || isSavingNote.value) return
  isSavingNote.value = true
  try {
    const { data } = await axios.post(`${API_BASE}/complaints/${route.params.id}/notes`,
      { text: newNote.value.trim() }, authHeaders())
    complaint.value.officerNotes = [data.note, ...(complaint.value.officerNotes || [])]
    newNote.value = ''
  } catch (err) {
    modalError.value = err.response?.data?.message || 'Failed to save note.'
  } finally {
    isSavingNote.value = false
  }
}
const deleteNote = async (noteId) => {
  try {
    await axios.delete(`${API_BASE}/complaints/${route.params.id}/notes/${noteId}`, authHeaders())
    complaint.value.officerNotes = (complaint.value.officerNotes || []).filter(n => n.id !== noteId)
  } catch (err) {
    modalError.value = err.response?.data?.message || 'Failed to delete note.'
  }
}

// Helper methods
const statusBadge = (status) => {
  const map = {
    'Assigned': 'bg-purple-100 text-purple-700',
    'In Progress': 'bg-amber-100 text-amber-700',
    'Resolved': 'bg-green-100 text-green-700',
    'Closed': 'bg-slate-200 text-slate-600',
    'Under Review': 'bg-blue-100 text-blue-700',
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