<template>
  <div class="q-pa-md">
    <q-form @submit="onSubmit" class="q-gutter-md">
      <q-input
        v-model="form.lastName"
        label="Фамилия"
      />
      
      <q-input
        v-model="form.firstName"
        label="Имя"
        :rules="[val => !!val || 'Обязательное поле']"
      />
      
      <q-input
        v-model="form.middleName"
        label="Отчество"
      />

      <q-select
        v-model="form.gender"
        :options="genderOptions"
        label="Пол"
        :rules="[val => !!val || 'Обязательное поле']"
      />

      <q-input
        v-model="form.birthDate"
        label="Дата рождения"
        type="date"
      />

      <q-input
        v-model="form.email"
        label="Email"
        type="email"
      />

      <div class="row justify-between">
        <q-btn
          label="Зарегистрироваться"
          type="submit"
          color="primary"
          class="full-width"
          :loading="loading"
        />
      </div>

      <div class="text-center q-mt-sm">
        <router-link to="/login" class="text-primary" style="text-decoration: none">
          Уже есть аккаунт? Войти
        </router-link>
      </div>
    </q-form>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import axios from 'axios'
import { useQuasar } from 'quasar'

const $q = useQuasar()
const loading = ref(false)

interface GenderOption {
  label: string
  value: 'male' | 'female'
}

const genderOptions: GenderOption[] = [
  { label: 'Мужской', value: 'male' },
  { label: 'Женский', value: 'female' }
]

interface RegistrationForm {
  lastName: string
  firstName: string
  middleName: string
  gender: GenderOption | null
  birthDate: string
  email: string
}

const form = ref<RegistrationForm>({
  lastName: 'Стронгов',
  firstName: 'Макс',
  middleName: 'Сергеевич',
  gender: { label: 'Мужской', value: 'male' },
  birthDate: '1990-01-01',
  email: 'max@example.com'
})

const onSubmit = async () => {
  try {
    loading.value = true
    
    // Проверяем только обязательные поля
    if (!form.value.firstName || !form.value.gender) {
      throw new Error('Пожалуйста, заполните имя и выберите пол')
    }

    console.log('before request')
    
    const response = await axios.post('http://localhost:8000/auth/register', {
      last_name: form.value.lastName || null,
      first_name: form.value.firstName,
      middle_name: form.value.middleName || null,
      gender: form.value.gender.value,
      birth_date: form.value.birthDate || null,
      email: form.value.email || null
    })

    console.log('after request')
    
    $q.notify({
      type: 'positive',
      message: 'Регистрация успешно начата'
    })
    console.log('Registration response:', response.data)
  } catch (error) {
    console.error('Registration error:', error)
    $q.notify({
      type: 'negative',
      message: 'Ошибка при регистрации'
    })
  } finally {
    loading.value = false
  }
}
</script> 