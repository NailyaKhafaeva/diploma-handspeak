<script>
    import {
        PUBLIC_API_URL
    } from "$env/static/public";
    import { onMount } from 'svelte';
    import axios from "axios";
    import { isAuthenticated } from "../stores.ts";


    let email = '';
    let password = '';
    let error = '';

    async function login() {
        try {
            const response = await axios.post(PUBLIC_API_URL + '/login', { email, password },
                { headers:
                        { 'Content-Type': 'application/json',
                            "Access-Control-Allow-Origin": "*"}
                });
            const result = response.data;
            if (!result.success) {
                error = result.error;
                return;
            }
            isAuthenticated.set('true');
            localStorage.setItem('token', result.token);
            alert('Login successful!');
            window.location.href = '/profile';
        } catch (error) {
            console.error(error);
            error = 'An error occurred. Please try again later.';
        }
    }

    onMount(() => {
        if (localStorage.getItem('token')) {
            window.location.href = '/profile';
        }
    });
</script>

<main>
    <body>
        <h2>Вход</h2>
        <form>
            <label for="email">Email:</label>
            <input type="text" id="email" bind:value={email}>
            <label for="password">Пароль:</label>
            <input type="password" id="password" bind:value={password}>
            <button on:click={login}>Войти</button>
        </form>
    </body>
</main>

<style>
    h2 {
        font-size: 2.5em;
        color: rgb(75, 110, 255);
        text-align: center;
    }

    form {
        max-width: 500px;
        margin: 0 auto;
        padding: 20px;
        border-radius: 6px;
        box-shadow: 0 5px 5px rgba(0, 0, 0, 0.3);
    }


    label {
        display: flex;
        margin-bottom: 8px;
        color: #3b3939;
    }

    input[type="text"],
    input[type="password"] {
        width: 100%;
        padding: 12px;
        border: none;
        border-radius: 4px;
        margin-bottom: 16px;
        box-sizing: border-box;
        background-color: #f5f5f5;
        font-size: 16px;
        color: #333;
    }

    button {
        background-color: rgb(75, 110, 255);
        color: #fff;
        margin: 0 auto;
        display: block;
        padding: 12px 24px;
        border: none;
        border-radius: 4px;
        cursor: pointer;
         font-size: 16px;
     }

     button:hover {
        background-color: rgb(75, 110, 255);
    }
</style>