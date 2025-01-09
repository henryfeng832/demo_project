<template>
  <div class="container mx-auto px-4 py-8">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold">User Management</h1>
      <button @click="openModal('add')" class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">
        Add User
      </button>
    </div>

    <!-- User Table -->
    <div class="overflow-x-auto">
      <table class="min-w-full bg-white">
        <thead>
          <tr>
            <th class="px-6 py-3 border-b-2 border-gray-200 text-left">ID</th>
            <th class="px-6 py-3 border-b-2 border-gray-200 text-left">Name</th>
            <th class="px-6 py-3 border-b-2 border-gray-200 text-left">Gender</th>
            <th class="px-6 py-3 border-b-2 border-gray-200 text-left">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id">
            <td class="px-6 py-4 border-b border-gray-200">{{ user.id }}</td>
            <td class="px-6 py-4 border-b border-gray-200">{{ user.name }}</td>
            <td class="px-6 py-4 border-b border-gray-200">{{ user.gender }}</td>
            <td class="px-6 py-4 border-b border-gray-200">
              <button @click="openModal('edit', user)" class="text-blue-500 hover:text-blue-700">
                Edit
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Pagination -->
    <div class="mt-4 flex justify-center">
      <button 
        @click="changePage(currentPage - 1)" 
        :disabled="currentPage === 1"
        class="mx-1 px-4 py-2 border rounded"
        :class="{ 'opacity-50 cursor-not-allowed': currentPage === 1 }"
      >
        Previous
      </button>
      <span class="mx-4 py-2">Page {{ currentPage }}</span>
      <button 
        @click="changePage(currentPage + 1)" 
        :disabled="!hasNextPage"
        class="mx-1 px-4 py-2 border rounded"
        :class="{ 'opacity-50 cursor-not-allowed': !hasNextPage }"
      >
        Next
      </button>
    </div>

    <!-- Modal -->
    <div v-if="showModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
      <div class="bg-white p-6 rounded-lg w-96">
        <h2 class="text-xl font-bold mb-4">{{ modalMode === 'add' ? 'Add User' : 'Edit User' }}</h2>
        <div class="mb-4">
          <label class="block text-sm font-medium mb-1">Name</label>
          <input 
            v-model="formData.name" 
            type="text" 
            class="w-full px-3 py-2 border rounded"
          >
        </div>
        <div class="mb-4">
          <label class="block text-sm font-medium mb-1">Gender</label>
          <select 
            v-model="formData.gender" 
            class="w-full px-3 py-2 border rounded"
          >
            <option value="male">Male</option>
            <option value="female">Female</option>
          </select>
        </div>
        <div class="flex justify-end">
          <button @click="closeModal" class="mr-2 px-4 py-2 border rounded">
            Cancel
          </button>
          <button @click="submitForm" class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">
            Confirm
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      users: [],
      currentPage: 1,
      totalUsers: 0,
      showModal: false,
      modalMode: 'add',
      formData: {
        id: null,
        name: '',
        gender: 'male'
      }
    }
  },
  computed: {
    hasNextPage() {
      return this.currentPage * 5 < this.totalUsers
    }
  },
  methods: {
    async fetchUsers() {
      try {
        const response = await axios.get(`${import.meta.env.VITE_API_URL}/api/users?page=${this.currentPage}`)
        this.users = response.data.users
        this.totalUsers = response.data.total
      } catch (error) {
        console.error('Error fetching users:', error)
      }
    },
    async submitForm() {
      try {
        if (this.modalMode === 'add') {
          await axios.post(`${import.meta.env.VITE_API_URL}/api/users`, this.formData)
        } else {
          await axios.put(`${import.meta.env.VITE_API_URL}/api/users/${this.formData.id}`, this.formData)
        }
        this.fetchUsers()
        this.closeModal()
      } catch (error) {
        console.error('Error submitting form:', error)
      }
    },
    openModal(mode, user = null) {
      this.modalMode = mode
      if (mode === 'edit' && user) {
        this.formData = { ...user }
      } else {
        this.formData = { id: null, name: '', gender: 'male' }
      }
      this.showModal = true
    },
    closeModal() {
      this.showModal = false
      this.formData = { id: null, name: '', gender: 'male' }
    },
    changePage(page) {
      if (page >= 1 && (page - 1) * 5 < this.totalUsers) {
        this.currentPage = page
        this.fetchUsers()
      }
    }
  },
  mounted() {
    this.fetchUsers()
  }
}
</script> 