import { describe, it, expect, vi } from 'vitest'
import { mount, flushPromises } from '@vue/test-utils'
import FormBuilder from '@/views/FormBuilder.vue'
import axios from 'axios'

// Mock Axios
vi.mock('axios')

describe('FormBuilder.vue', () => {
    it('adds a draft section when "Add Section" is clicked', async () => {
        // Arrange
        const wrapper = mount(FormBuilder)

        // Act: Type section name
        const input = wrapper.find('input[placeholder="New Section Name"]')
        await input.setValue('Personal Info')

        // Act: Click Add
        const addButton = wrapper.find('button.bg-blue-600') // Adjust selector if needed
        await addButton.trigger('click')

        // Assert: Check if section is in the list
        expect(wrapper.vm.draftSections).toHaveLength(1)
        expect(wrapper.vm.draftSections[0].name).toBe('Personal Info')
        expect(wrapper.text()).toContain('Personal Info')
    })

    it('includes draft sections in the create form payload', async () => {
        // Arrange
        const wrapper = mount(FormBuilder)

        // Fill Form Name
        await wrapper.find('input[placeholder="e.g. Employee Onboarding"]').setValue('Test Form')

        // Add a Draft Section
        const input = wrapper.find('input[placeholder="New Section Name"]')
        await input.setValue('Section A')
        await wrapper.find('button.bg-blue-600').trigger('click') // Add Section

        // Mock API Success
        axios.post.mockResolvedValue({ data: { id: 1 } })
        axios.get.mockResolvedValue({ data: [] }) // For fetchTemplates

        // Act: Submit Form
        await wrapper.find('form').trigger('submit.prevent')
        await flushPromises()

        // Assert: Check Axios Payload
        expect(axios.post).toHaveBeenCalledTimes(1)
        const payload = axios.post.mock.calls[0][1]
        expect(payload.name).toBe('Test Form')
        expect(payload.sections).toHaveLength(1)
        expect(payload.sections[0].name).toBe('Section A')
    })
})
