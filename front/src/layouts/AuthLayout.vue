<template>
  <q-layout view="hHh lpR fFf">
    <q-page-container class="auth-container">
      <div class="row items-center justify-center" style="min-height: 100vh;">
        <div class="col-12 col-sm-8 col-md-6 col-lg-4">
          <q-card flat bordered class="auth-card q-pa-lg">
            <div class="text-center q-mb-lg">
              <router-link to="/" class="text-black" style="text-decoration: none">
                <div class="text-h4 q-mb-md">Assistant</div>
              </router-link>
            </div>
            <router-view />
          </q-card>
        </div>
      </div>
    </q-page-container>
  </q-layout>
</template>

<script setup lang="ts">
</script>

<style lang="scss">
.auth-container {
  background: #f5f5f5;
  min-height: 100vh;
}

.auth-card {
  background: white;
  border-radius: 8px;
}
</style> 