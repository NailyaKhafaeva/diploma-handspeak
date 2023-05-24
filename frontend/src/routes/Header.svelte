<script>
	import { page } from '$app/stores';
	import { isAuthenticated } from "./stores.ts";
	import { browser } from "$app/environment";

	function logout() {
		localStorage.removeItem('token');
		isAuthenticated.set('false');
		window.location.href = '/login';
	}
</script>

<main>
	<div>
		{#if (browser && (localStorage.getItem("isAuth") === 'true'))}
			<header>
				<nav>
					<ul>
						<li aria-current={$page.url.pathname === '/profile' ? 'page' : undefined}>
							<a href="/profile">Профиль</a>
						</li>
						<li aria-current={$page.url.pathname === '/levels' ? 'page' : undefined}>
							<a href="/levels">Уровни</a>
						</li>
					</ul>
				</nav>
				<nav class="right_nav">
					<button on:click={logout}>Выход</button>
				</nav>
			</header>
		{:else}
			<header>
				<nav>
					<ul>
						<li aria-current={$page.url.pathname === '/' ? 'page' : undefined}>
							<a href="/">Начальная страница</a>
						</li>
						<li aria-current={$page.url.pathname === '/signup' ? 'page' : undefined}>
							<a href="/signup">Регистрация</a>
						</li>
						<li aria-current={$page.url.pathname === '/login' ? 'page' : undefined}>
							<a href="/login">Вход</a>
						</li>
					</ul>
				</nav>
			</header>
		{/if}
	</div>
</main>

<style>
	header {
		display: block;
		justify-content: space-between;
	}

	nav {
		display: block;
		justify-content: right;
		--background: rgb(75, 110, 255);
	}

	ul {
		position: relative;
		padding: 1em;
		margin: 0;
		height: 3em;
		display: flex;
		justify-content: center;
		align-items: center;
		list-style: none;
		background: var(--background);
		background-size: contain;
	}

	li {
		position: relative;
		height: 100%;
	}

	li[aria-current='page']::before {
		--size: 6px;
		content: '';
		width: 0;
		height: 0;
		position: absolute;
		top: 0;
		left: calc(50% - var(--size));
		border: var(--size) solid transparent;
		border-top: var(--size) solid var(--color-theme-2);
	}

	nav a {
		display: flex;
		height: 100%;
		align-items: center;
		padding: 0 0.5rem;
		color: var(--color-text);
		font-weight: 700;
		font-size: 0.8rem;
		text-transform: uppercase;
		letter-spacing: 0.1em;
		text-decoration: none;
		transition: color 0.2s linear;
	}

	a:hover {
		color: var(--color-theme-1);
	}

	button {
		display: flex;
		height: 100%;
		align-items: center;
		padding: 0 0.5rem;
		color: #3081ef;
		font-weight: 700;
		font-size: 0.8rem;
		text-transform: uppercase;
		letter-spacing: 0.1em;
		text-decoration: none;
		transition: color 0.2s linear;
	}

	.right_nav {
		display: flex;
		justify-content: right;
		--background: rgb(75, 110, 255);
	}
</style>
