<script>
    export let data;
    const { lessons } = data;
    let currentLevel = lessons[0];
</script>

<main>
    <div>
        <h3 style="color: #333333">Уровень {currentLevel.level_id}</h3>
        <hr>
    </div>

    {#each lessons as lesson}
        <div>
            <a href="/levels/{lesson.level_id}/{lesson.id}">
                <h3>{lesson.name}</h3>
            </a>
            <h4>{lesson.description}</h4>
            <hr>
        </div>
    {/each}
</main>

<style>
    h1 {
        text-align: initial;
        color: #333333;
    }
    h3 {
        text-align: initial;
        color: #4b6eff;
    }

    h4 {
        text-align: initial;
        color: #809dff;
    }
</style>