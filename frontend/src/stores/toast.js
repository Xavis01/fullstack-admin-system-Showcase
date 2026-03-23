import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useToastStore = defineStore('toast', () => {
    // State
    const toasts = ref([]);

    /**
     * Add a new toast notification
     * @param {Object} toast - The toast object
     * @param {string} toast.title - Title of the toast
     * @param {string} toast.message - Body message of the toast
     * @param {'success' | 'error' | 'warning' | 'info'} toast.type - Type of toast
     * @param {number} [toast.duration=5000] - Duration in ms before auto-dismiss
     */
    function add(toast) {
        const id = Date.now() + Math.random().toString(36).substring(2, 9);
        const newToast = {
            id,
            title: toast.title,
            message: toast.message,
            type: toast.type || 'info', // default to info
            duration: toast.duration || 5000,
        };

        toasts.value.push(newToast);

        if (newToast.duration > 0) {
            setTimeout(() => {
                remove(id);
            }, newToast.duration);
        }
    }

    /**
     * Remove a toast by ID
     * @param {string} id - The ID of the toast to remove
     */
    function remove(id) {
        const index = toasts.value.findIndex((t) => t.id === id);
        if (index !== -1) {
            toasts.value.splice(index, 1);
        }
    }

    return {
        toasts,
        add,
        remove,
    };
});
