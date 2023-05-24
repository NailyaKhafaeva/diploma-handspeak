import {writable} from "svelte/store";
import {browser} from "$app/environment";

export const isAuthenticated = writable(
    browser && (localStorage.getItem("isAuth") || "false")
);

isAuthenticated.subscribe((val) => browser && localStorage.setItem("isAuth", val === 'false' ? 'false' : 'true'));
