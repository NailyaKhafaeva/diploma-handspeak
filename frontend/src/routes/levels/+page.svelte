<script>
    export let data;
    const { levels } = data;
</script>

<main>
    {#each levels as level}
        <div>
            <a href="/levels/{level.id}" >
                <h3>{level.name}</h3>
            </a>

            <h4>&nbsp &nbsp{level.description}</h4>
            <hr>
        </div>
    {/each}
</main>


<style>
    h3 {
        text-align: initial;
        color: #4b6eff;
    }

    h4 {
        text-align: initial;
        color: #809dff;
    }
</style>