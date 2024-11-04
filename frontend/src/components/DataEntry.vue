<template>
    <div class="container mt-5">
      <h2 class="mb-4">Add User</h2>
      <form @submit.prevent="submitData" class="mb-4">
        <div class="form-row">
          <div class="form-group col-md-6">
            <label for="name">Name:</label>
            <input type="text" class="form-control" v-model="name" required />
          </div>
          <div class="form-group col-md-6">
            <label for="email">Email:</label>
            <input type="email" class="form-control" v-model="email" required />
          </div>
        </div>
        <button type="submit" class="btn btn-primary">
          {{ editMode ? 'Update' : 'Submit' }}
        </button>
        <p v-if="message" class="mt-3 text-success">{{ message }}</p>
      </form>
  
      <h3 class="mt-5">User List</h3>
      <div class="table-responsive">
        <table class="table table-bordered mt-3" style="min-width: 800px;">
          <thead class="thead-light">
            <tr>
              <th>Name</th>
              <th>Email</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in users" :key="user.id">
              <td>{{ user.name }}</td>
              <td>{{ user.email }}</td>
              <td>
                <button class="btn btn-warning btn-sm" @click="editUser(user)">Edit</button>
                <button class="btn btn-danger btn-sm" @click="deleteUser(user.id)">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        name: '',
        email: '',
        message: '',
        users: [],
        editMode: false,
        currentUserId: null,
      };
    },
    async mounted() {
      await this.fetchUsers();
    },
    methods: {
      async fetchUsers() {
        try {
          const response = await fetch('http://localhost:5000/users');
          if (!response.ok) {
            throw new Error('Failed to fetch users');
          }
          this.users = await response.json();
        } catch (error) {
          console.error('Error fetching users:', error);
        }
      },
      async submitData() {
        const url = this.editMode ? `http://localhost:5000/edit/${this.currentUserId}` : 'http://localhost:5000/add';
        const method = this.editMode ? 'PUT' : 'POST';
  
        try {
          const response = await fetch(url, {
            method,
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({
              name: this.name,
              email: this.email
            })
          });
  
          if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.message || 'Network response was not ok');
          }
  
          const data = await response.json();
          this.message = data.message;
  
          await this.fetchUsers();
          this.resetForm();
        } catch (error) {
          this.message = 'Error: ' + error.message;
        }
      },
      editUser(user) {
        this.name = user.name;
        this.email = user.email;
        this.currentUserId = user.id;
        this.editMode = true;
      },
      async deleteUser(id) {
        try {
          const response = await fetch(`http://localhost:5000/delete/${id}`, {
            method: 'DELETE'
          });
  
          if (!response.ok) {
            throw new Error('Failed to delete user');
          }
  
          const data = await response.json();
          this.message = data.message;
  
          await this.fetchUsers();
        } catch (error) {
          this.message = 'Error: ' + error.message;
        }
      },
      resetForm() {
        this.name = '';
        this.email = '';
        this.currentUserId = null;
        this.editMode = false;
      }
    }
  };
  </script>
  
  <style scoped>
  .table-responsive {
    overflow-x: auto; 
  }
  
  .btn {
    margin-right: 5px;
  }
  </style>
  