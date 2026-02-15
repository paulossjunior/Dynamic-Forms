<template>
  <div class="space-y-6">
    <!-- Render Sections -->
    <div v-for="section in sortedSections" :key="section.id">
      <FormSection :section="section">
        <div v-for="field in groupedFields[section.id]" :key="field.key_name">
          <label :for="field.key_name" class="block text-sm font-medium text-gray-700 mb-1">
            {{ field.label }}
            <span v-if="isRequired(field)" class="text-red-500">*</span>
          </label>
          
          <div class="field-wrapper">
             <template v-if="['text', 'number', 'date', 'email'].includes(field.field_type)">
                <input
                  :type="field.field_type"
                  :id="field.key_name"
                  :value="modelValue[field.key_name]"
                  @input="updateValue(field.key_name, $event.target.value)"
                  class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm"
                  :class="{'border-red-300 focus:ring-red-500 focus:border-red-500': errors[field.key_name]}"
                />
             </template>

             <template v-else-if="field.field_type === 'select'">
                <Listbox
                  :modelValue="modelValue[field.key_name]"
                  @update:modelValue="val => updateValue(field.key_name, val)"
                >
                  <div class="relative mt-1">
                    <ListboxButton
                      class="relative w-full cursor-default rounded-md border border-gray-300 bg-white py-2 pl-3 pr-10 text-left shadow-sm focus:border-green-500 focus:outline-none focus:ring-1 focus:ring-green-500 sm:text-sm"
                      :class="{'border-red-300 focus:ring-red-500 focus:border-red-500': errors[field.key_name]}"
                    >
                      <span class="block truncate">
                        {{ modelValue[field.key_name] || 'Select an option' }}
                      </span>
                      <span class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2">
                        <ChevronUpDownIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
                      </span>
                    </ListboxButton>

                    <transition
                      leave-active-class="transition duration-100 ease-in"
                      leave-from-class="opacity-100"
                      leave-to-class="opacity-0"
                    >
                      <ListboxOptions
                        class="absolute z-10 mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm"
                      >
                        <ListboxOption
                          v-for="opt in parseOptions(field.options)"
                          :key="opt"
                          :value="opt"
                          as="template"
                          v-slot="{ active, selected }"
                        >
                          <li
                            :class="[
                              active ? 'bg-green-100 text-green-900' : 'text-gray-900',
                              'relative cursor-default select-none py-2 pl-10 pr-4',
                            ]"
                          >
                            <span
                              :class="[
                                selected ? 'font-medium' : 'font-normal',
                                'block truncate',
                              ]"
                            >
                              {{ opt }}
                            </span>
                            <span
                              v-if="selected"
                              class="absolute inset-y-0 left-0 flex items-center pl-3 text-green-600"
                            >
                              <CheckIcon class="h-5 w-5" aria-hidden="true" />
                            </span>
                          </li>
                        </ListboxOption>
                      </ListboxOptions>
                    </transition>
                  </div>
                </Listbox>
             </template>

             <template v-else-if="field.field_type === 'multiselect'">
                 <Listbox
                    :modelValue="modelValue[field.key_name] || []"
                    @update:modelValue="val => updateMultiSelect(field.key_name, val)"
                    multiple
                  >
                    <div class="relative mt-1">
                      <ListboxButton
                        class="relative w-full cursor-default rounded-md border border-gray-300 bg-white py-2 pl-3 pr-10 text-left shadow-sm focus:border-green-500 focus:outline-none focus:ring-1 focus:ring-green-500 sm:text-sm min-h-[38px]"
                        :class="{'border-red-300 focus:ring-red-500 focus:border-red-500': errors[field.key_name]}"
                      >
                        <span class="block truncate">
                          <span v-if="!modelValue[field.key_name] || modelValue[field.key_name].length === 0" class="text-gray-500">Select options...</span>
                          <span v-else>
                              {{ modelValue[field.key_name].join(', ') }}
                          </span>
                        </span>
                        <span class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2">
                          <ChevronUpDownIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
                        </span>
                      </ListboxButton>
          
                      <transition
                        leave-active-class="transition duration-100 ease-in"
                        leave-from-class="opacity-100"
                        leave-to-class="opacity-0"
                      >
                        <ListboxOptions
                          class="absolute z-10 mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm"
                        >
                          <ListboxOption
                            v-for="opt in parseOptions(field.options)"
                            :key="opt"
                            :value="opt"
                            as="template"
                            v-slot="{ active, selected }"
                          >
                            <li
                              :class="[
                                active ? 'bg-green-100 text-green-900' : 'text-gray-900',
                                'relative cursor-default select-none py-2 pl-10 pr-4',
                              ]"
                            >
                              <span
                                :class="[
                                  selected ? 'font-medium' : 'font-normal',
                                  'block truncate',
                                ]"
                              >
                                {{ opt }}
                              </span>
                              <span
                                v-if="selected"
                                class="absolute inset-y-0 left-0 flex items-center pl-3 text-green-600"
                              >
                                <CheckIcon class="h-5 w-5" aria-hidden="true" />
                              </span>
                            </li>
                          </ListboxOption>
                        </ListboxOptions>
                      </transition>
                    </div>
                  </Listbox>
             </template>
          </div>
          
          <p v-if="errors[field.key_name]" class="mt-1 text-sm text-red-600">
            {{ errors[field.key_name] }}
          </p>
        </div>
      </FormSection>
    </div>

    <!-- Render Unsectioned Fields -->
    <div v-if="unsectionedFields.length > 0" class="space-y-6">
       <div v-for="field in unsectionedFields" :key="field.key_name">
          <label :for="field.key_name" class="block text-sm font-medium text-gray-700 mb-1">
            {{ field.label }}
            <span v-if="isRequired(field)" class="text-red-500">*</span>
          </label>
          
          <div class="field-wrapper">
             <!-- Same pattern for unsectioned fields -->
             <template v-if="['text', 'number', 'date', 'email'].includes(field.field_type)">
                <input
                  :type="field.field_type"
                  :id="field.key_name"
                  :value="modelValue[field.key_name]"
                  @input="updateValue(field.key_name, $event.target.value)"
                  class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm"
                  :class="{'border-red-300 focus:ring-red-500 focus:border-red-500': errors[field.key_name]}"
                />
             </template>
             <!-- ... other types omitted for brevity in thought, but I will include them in full write_to_file ... -->
             <!-- Selection (reusing logic) -->
              <template v-else-if="field.field_type === 'select'">
                <Listbox
                  :modelValue="modelValue[field.key_name]"
                  @update:modelValue="val => updateValue(field.key_name, val)"
                >
                  <div class="relative mt-1">
                    <ListboxButton
                      class="relative w-full cursor-default rounded-md border border-gray-300 bg-white py-2 pl-3 pr-10 text-left shadow-sm focus:border-green-500 focus:outline-none focus:ring-1 focus:ring-green-500 sm:text-sm"
                      :class="{'border-red-300 focus:ring-red-500 focus:border-red-500': errors[field.key_name]}"
                    >
                      <span class="block truncate">
                        {{ modelValue[field.key_name] || 'Select an option' }}
                      </span>
                      <span class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2">
                        <ChevronUpDownIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
                      </span>
                    </ListboxButton>

                    <transition
                      leave-active-class="transition duration-100 ease-in"
                      leave-from-class="opacity-100"
                      leave-to-class="opacity-0"
                    >
                      <ListboxOptions
                        class="absolute z-10 mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm"
                      >
                        <ListboxOption
                          v-for="opt in parseOptions(field.options)"
                          :key="opt"
                          :value="opt"
                          as="template"
                          v-slot="{ active, selected }"
                        >
                          <li
                            :class="[
                              active ? 'bg-green-100 text-green-900' : 'text-gray-900',
                              'relative cursor-default select-none py-2 pl-10 pr-4',
                            ]"
                          >
                            <span
                              :class="[
                                selected ? 'font-medium' : 'font-normal',
                                'block truncate',
                              ]"
                            >
                              {{ opt }}
                            </span>
                            <span
                              v-if="selected"
                              class="absolute inset-y-0 left-0 flex items-center pl-3 text-green-600"
                            >
                              <CheckIcon class="h-5 w-5" aria-hidden="true" />
                            </span>
                          </li>
                        </ListboxOption>
                      </ListboxOptions>
                    </transition>
                  </div>
                </Listbox>
             </template>

             <template v-else-if="field.field_type === 'multiselect'">
                 <Listbox
                    :modelValue="modelValue[field.key_name] || []"
                    @update:modelValue="val => updateMultiSelect(field.key_name, val)"
                    multiple
                  >
                    <div class="relative mt-1">
                      <ListboxButton
                        class="relative w-full cursor-default rounded-md border border-gray-300 bg-white py-2 pl-3 pr-10 text-left shadow-sm focus:border-green-500 focus:outline-none focus:ring-1 focus:ring-green-500 sm:text-sm min-h-[38px]"
                        :class="{'border-red-300 focus:ring-red-500 focus:border-red-500': errors[field.key_name]}"
                      >
                        <span class="block truncate">
                          <span v-if="!modelValue[field.key_name] || modelValue[field.key_name].length === 0" class="text-gray-500">Select options...</span>
                          <span v-else>
                              {{ modelValue[field.key_name].join(', ') }}
                          </span>
                        </span>
                        <span class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2">
                          <ChevronUpDownIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
                        </span>
                      </ListboxButton>
          
                      <transition
                        leave-active-class="transition duration-100 ease-in"
                        leave-from-class="opacity-100"
                        leave-to-class="opacity-0"
                      >
                        <ListboxOptions
                          class="absolute z-10 mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm"
                        >
                          <ListboxOption
                            v-for="opt in parseOptions(field.options)"
                            :key="opt"
                            :value="opt"
                            as="template"
                            v-slot="{ active, selected }"
                          >
                            <li
                              :class="[
                                active ? 'bg-green-100 text-green-900' : 'text-gray-900',
                                'relative cursor-default select-none py-2 pl-10 pr-4',
                              ]"
                            >
                              <span
                                :class="[
                                  selected ? 'font-medium' : 'font-normal',
                                  'block truncate',
                                ]"
                              >
                                {{ opt }}
                              </span>
                              <span
                                v-if="selected"
                                class="absolute inset-y-0 left-0 flex items-center pl-3 text-green-600"
                              >
                                <CheckIcon class="h-5 w-5" aria-hidden="true" />
                              </span>
                            </li>
                          </ListboxOption>
                        </ListboxOptions>
                      </transition>
                    </div>
                  </Listbox>
             </template>
          </div>
          
          <p v-if="errors[field.key_name]" class="mt-1 text-sm text-red-600">
            {{ errors[field.key_name] }}
          </p>
       </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import {
  Listbox,
  ListboxButton,
  ListboxOptions,
  ListboxOption,
} from '@headlessui/vue'
import { CheckIcon, ChevronUpDownIcon } from '@heroicons/vue/20/solid'
import FormSection from '../Section/FormSection.vue'

const props = defineProps({
  fields: {
    type: Array,
    default: () => []
  },
  sections: {
    type: Array,
    default: () => []
  },
  modelValue: {
    type: Object,
    default: () => ({})
  },
  errors: {
    type: Object,
    default: () => ({})
  }
})

const emit = defineEmits(['update:modelValue'])

const sortedSections = computed(() => {
  return [...props.sections].sort((a, b) => (a.order_index || 0) - (b.order_index || 0))
})

const groupedFields = computed(() => {
  const groups = {}
  props.fields.forEach(field => {
    if (field.section_id) {
      if (!groups[field.section_id]) groups[field.section_id] = []
      groups[field.section_id].push(field)
    }
  })
  return groups
})

const unsectionedFields = computed(() => {
  return props.fields.filter(f => !f.section_id)
})

const updateValue = (key, value) => {
  const newData = { ...props.modelValue, [key]: value }
  emit('update:modelValue', newData)
}

const updateMultiSelect = (key, value) => {
  const newData = { ...props.modelValue, [key]: value }
  emit('update:modelValue', newData)
}

const parseOptions = (options) => {
  if (Array.isArray(options)) return options
  if (typeof options === 'string') {
    try {
      return JSON.parse(options)
    } catch (e) {
      return []
    }
  }
  return []
}

const isRequired = (field) => {
  try {
    const rules = typeof field.validation_rules === 'string' 
      ? JSON.parse(field.validation_rules) 
      : field.validation_rules || {}
    return !!rules.required
  } catch {
    return false
  }
}
</script>
