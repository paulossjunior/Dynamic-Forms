import { describe, it, expect, vi } from 'vitest'
import { mount, flushPromises } from '@vue/test-utils'
import PersonCreate from '@/views/PersonCreate.vue'
import axios from 'axios'
import { createRouter, createWebHistory } from 'vue-router'

// Mock Axios
vi.mock('axios')

// Mock Router
const router = createRouter({
    history: createWebHistory(),
    routes: [{ path: '/', component: { template: '<div>Home</div>' } }]
})

describe('PersonCreate.vue', () => {
    it('displays error message when API returns 400 Bad Request', async () => {
        // Arrange
        const wrapper = mount(PersonCreate, {
            global: {
                plugins: [router]
            }
        })

        // Fill form
        await wrapper.find('#name').setValue('Test User')
        await wrapper.find('#email').setValue('duplicate@example.com')

        // Mock API Error
        axios.post.mockRejectedValue({
            response: {
                status: 400,
                data: { detail: 'A person with this email already exists.' }
            }
        })

        // Act
        await wrapper.find('form').trigger('submit.prevent')
        await flushPromises()

        // Assert
        // Verify alert was NOT called (we want on-screen error)
        // Note: We can't easily mock window.alert in jsdom without setup, but we check for UI element

        // Check for error message on screen
        // We expect an element with text "A person with this email already exists."
        expect(wrapper.text()).toContain('A person with this email already exists.')

        // Optional: Check if it has error styling (e.g., text-red-700)
        const errorMsg = wrapper.find('.text-red-700')
        expect(errorMsg.exists()).toBe(true)
    })
})
