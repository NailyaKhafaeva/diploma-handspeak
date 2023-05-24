<script>
	import axios from "axios";
	import {
		PUBLIC_API_URL
	} from "$env/static/public";


  	let username = '';
  	let email = '';
  	let password = '';

	async function registerUser() {
		try {
			const response = await axios.post(PUBLIC_API_URL + '/signup', { username, email, password },
					{ headers:
								{ 'Content-Type': 'application/json',
									"Access-Control-Allow-Origin": "*" }
					});

			if (response.status === 201) {
				alert('Registration successful!');
				username = '';
				email = '';
				password = '';
			} else {
				alert('Registration failed!');
			}
		} catch (error) {
			alert('Registration failed! Error: ' + error.message);
		}
	}
</script>

<main>
	<body>
		<h2>Регистрация</h2>
		<form on:submit={registerUser}>
		  <label for="username">Имя:</label>
		  <input type="text" id="username" bind:value={username} required>
		  <label for="email">Email:</label>
		  <input type="email" id="email" bind:value={email} required>
		  <label for="password">Пароль:</label>
		  <input type="password" id="password" bind:value={password} required>
		  <button type="submit">Зарегистрироваться</button>
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
		box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
	}

	label {
		display: flex;
		margin-bottom: 8px;
		color: #3b3939;
	}

	input[type="text"],
	input[type="email"],
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

	button[type="submit"] {
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

	button[type="submit"]:hover {
		background-color: rgb(75, 110, 255);
	}
</style>