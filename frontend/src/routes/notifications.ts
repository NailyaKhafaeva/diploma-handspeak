import type {Writable} from "svelte/store";
import {derived, writable} from "svelte/store";

const TIMEOUT = 3000

function createNotificationStore (timeout: number) {
    const _notifications: Writable<any[]> = writable([])

    function send (message: string, type = "default", timeout: number) {
        _notifications.update((state: any[]) => {
            return [...state, { id: id(), type, message, timeout }]
        })
    }

    let timers = []

    const notifications = derived<any, any>(_notifications, ($_notifications, set) => {
        set($_notifications)
        if (($_notifications as [])?.length > 0) {
            const timer = setTimeout(() => {
                _notifications.update(state => {
                    state.shift()
                    return state
                })
            }, ($_notifications as [any])[0] ? ($_notifications as [any])[0].timeout : 0)
            return () => {
                clearTimeout(timer)
            }
        }
    })
    const { subscribe } = notifications


    return {
        subscribe,
        send,
        success: (msg: string, timeout: number) => send(msg, "success", timeout),
        danger: (msg: string, timeout: number) => send(msg, "danger", timeout),
    }
}

function id() {
    return '_' + Math.random().toString(36).substr(2, 9);
};

export const notifications = createNotificationStore(TIMEOUT)