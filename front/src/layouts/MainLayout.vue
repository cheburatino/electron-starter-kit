<template>
  <q-layout view="hHh lpR fFf">
    <q-header elevated>
      <q-toolbar class="bg-white text-black">
        <q-btn flat dense round icon="menu" @click="leftDrawerOpen = !leftDrawerOpen" />
        <q-toolbar-title>
          <router-link to="/" style="text-decoration: none; color: inherit">
            Assistant
          </router-link>
        </q-toolbar-title>
        <q-btn
          flat
          no-caps
          to="/auth/registration"
          label="Регистрация"
          color="primary"
        />
      </q-toolbar>
    </q-header>

    <!-- Левый выдвижной Drawer -->
    <q-drawer show-if-above v-model="leftDrawerOpen" side="left" bordered>
      <q-list padding>
        <router-link to="/task" style="text-decoration: none; color: inherit">
          <q-item clickable v-ripple>
            <q-item-section avatar>
              <q-avatar size="40px">
                <img src="~assets/task.png" />
              </q-avatar>
            </q-item-section>
            <q-item-section>Задачи</q-item-section>
          </q-item>
        </router-link>
      </q-list>
    </q-drawer>
    <!-- Основная часть приложения (router-view) -->
    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup lang="ts">
import { ref } from 'vue'

// Управляем состоянием открытия/закрытия левого меню
const leftDrawerOpen = ref(false)
</script>
