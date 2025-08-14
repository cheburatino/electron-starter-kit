<template>
  <div class="welcome-page">
    <!-- Wrapper -->
    <main class="welcome-main">
      <!-- Logo / Title -->
      <h1 class="welcome-title">
        TYPESCAN
      </h1>

      <!-- CTA Buttons -->
      <div class="welcome-buttons">
        <q-btn
          color="primary"
          icon="login"
          label="Войти"
          rounded
          size="md"
          class="welcome-btn-primary"
          @click="handleLogin"
        />
        <q-btn
          color="white"
          text-color="grey-8"
          icon="person_add"
          label="Регистрация"
          rounded
          size="md"
          outline
          class="welcome-btn-secondary"
          @click="handleRegister"
        />
      </div>
    </main>

    <!-- Footer -->
    <footer class="welcome-footer">
      <span>© 2025 TYPESCAN</span>
      <nav class="welcome-nav">
        <a href="#" class="welcome-link">Политика</a>
        <a href="#" class="welcome-link">Контакты</a>
      </nav>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router';

const router = useRouter();

const handleLogin = () => {
  // Здесь будет логика для входа
  console.log('Вход в систему');
};

const handleRegister = () => {
  router.push('/auth/registration');
};
</script>

<style lang="scss" scoped>
.welcome-page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #eef2ff 0%, #ffffff 50%, #ecfdf5 100%);
  color: #111827;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'SF Pro Text', 'Helvetica Neue', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.welcome-main {
  width: 100%;
  max-width: 32rem;
  margin: 0 auto;
  padding: 0 1.5rem;
  text-align: center;
  display: flex;
  flex-direction: column;
  gap: 2.5rem;
}

.welcome-title {
  font-size: 2.25rem;
  font-weight: 600;
  letter-spacing: -0.025em;
  margin: 0;
  animation: fadeIn 0.8s ease-out;
  
  @media (min-width: 768px) {
    font-size: 3rem;
  }
}

.welcome-buttons {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  animation: fadeIn 0.8s ease-out 0.1s both;
  
  @media (min-width: 640px) {
    flex-direction: row;
  }
}

.welcome-btn-primary {
  padding: 0.75rem 1.5rem;
  font-size: 0.875rem;
  font-weight: 500;
  transition: all 0.2s ease;
  
  &:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(99, 102, 241, 0.25);
  }
}

.welcome-btn-secondary {
  padding: 0.75rem 1.5rem;
  font-size: 0.875rem;
  font-weight: 500;
  transition: all 0.2s ease;
  border: 1px solid #d1d5db;
  background: white;
  
  &:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    background: #f9fafb;
  }
}

.welcome-footer {
  width: 100%;
  max-width: 32rem;
  margin: 0 auto;
  padding: 0 1.5rem;
  margin-top: 4rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 0.75rem;
  color: #6b7280;
  border-top: 1px solid #e5e7eb;
  padding-top: 1.5rem;
}

.welcome-nav {
  display: flex;
  gap: 1rem;
}

.welcome-link {
  color: #6b7280;
  text-decoration: none;
  transition: color 0.2s ease;
  
  &:hover {
    color: #374151;
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style> 