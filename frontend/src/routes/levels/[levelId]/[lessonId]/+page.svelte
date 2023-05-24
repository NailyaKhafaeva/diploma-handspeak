<script>
    import axios from "axios";
    import { onMount } from "svelte";
    import { notifications } from "../../../notifications.ts";
    import {
        PUBLIC_API_URL
    } from "$env/static/public";
    import Toast from "../../../Toast.svelte";
    import Image11 from '$lib/images/level1lesson1.jpg'
    import Image12 from '$lib/images/level1lesson2.png'
    import Image21 from '$lib/images/level2lesson1.png'
    import Image22 from '$lib/images/level2lesson2.png'
    import Image23 from '$lib/images/level2lesson3.png'
    import Image24 from '$lib/images/level2lesson4.png'
    import Image25 from '$lib/images/level2lesson5.png'
    export let data;
    const { lesson } = data;

    let progressValue = 0;
    let counter = 0;
    let level_id = lesson[0].level_id;
    let lesson_id = lesson[0].id;
    let video;
    let photo = null;

    let stream;
    let canvas;
    let startbutton = null;
    let i = 0;

    let numbers = []
    let letters_map = {}

    function getRandomInt(min, max) {
        min = Math.ceil(min);
        max = Math.floor(max);
        return Math.floor(Math.random() * (max - min)) + min;
    }

    if (level_id === 1) {
        if (lesson_id === 1) {
            numbers = [0, 1, 2, 3, 4]
            for (let step = 0; step < 15; step++) {
                numbers.push(getRandomInt(0, 5))
            }
        } else if (lesson_id === 2) {
            numbers = [5, 6, 7, 8, 9]
            for (let step = 0; step < 15; step++) {
                numbers.push(getRandomInt(5, 10))
            }
        }
    } else if (level_id === 2) {
        if (lesson_id === 3) {
            letters_map = {0: 'A', 1: 'B', 2: 'Г', 3: 'Е', 4: 'Ж'}
            numbers = [0, 1, 2, 3, 4]
            for (let step = 0; step < 15; step++) {
                numbers.push(getRandomInt(0, 5))
            }
        } else if (lesson_id === 4) {
            letters_map = {5: 'И', 6: 'Л', 7: 'М', 8: 'Н', 9: 'О'}
            numbers = [5, 6, 7, 8, 9]
            for (let step = 0; step < 15; step++) {
                numbers.push(getRandomInt(5, 10))
            }
        } else if (lesson_id === 5) {
            letters_map = {10: 'П', 11: 'Р', 12: 'С', 13: 'Т', 14: 'У'}
            numbers = [10, 11, 12, 13, 14]
            for (let step = 0; step < 15; step++) {
                numbers.push(getRandomInt(10, 15))
            }
        } else if (lesson_id === 6) {
            letters_map = {15: 'Ф', 16: 'Х', 17: 'Ч', 18: 'Ш', 19: 'Ы'}
            numbers = [15, 16, 17, 18, 19]
            for (let step = 0; step < 15; step++) {
                numbers.push(getRandomInt(15, 20))
            }
        } else if (lesson_id === 7) {
            letters_map = {20: 'Э', 21: 'Ю', 22: 'Я'}
            numbers = [20, 21, 22]
            for (let step = 0; step < 15; step++) {
                numbers.push(getRandomInt(20, 23))
            }
        }
    }
    let number = numbers[i];

    async function getStream() {
        video = document.getElementById("video");
        canvas = document.getElementById("canvas");
        photo = document.getElementById("photo");
        startbutton = document.getElementById("startbutton");

        try {
            stream = await navigator.mediaDevices.getUserMedia({
                video: true,
                audio: false
            });
            video.srcObject = stream;
            video.play()
            const context = canvas.getContext ('2d');
            const borderX1 = 12;
            const borderY1 = 52;
            const borderX2 = 160;
            const borderY2 = 202;
            context.clearRect (0, 0, canvas.width, canvas.height);
            context.drawImage (video, 0, 0, canvas.width, canvas.height);
            context.strokeStyle = 'blue';
            context.lineWidth = 4;
            context.strokeRect (borderX1, borderY1, borderX2 - borderX1, borderY2 - borderY1);
        } catch (err) {
            console.error(err);
        }
    }
    async function progressUpdate() {
        const token = localStorage.getItem('token')
        const config = {
            headers: {
                'Content-Type': 'application/json',
                'token': `Bearer ${token}`
            }
        };

        try {
            const response = await axios.post(PUBLIC_API_URL + '/update_progress', { lesson_id, progressValue }, config);
            const result = response.data;

            if (result.success) {
                notifications.success('Ваш прогресс сохранен', 3000)

            } else {
                notifications.danger('Произошла ошибка, прогресс не сохранился', 3000)
            }
        } catch (error) {
            console.error(error);
        }
    }

    async function stopStream() {
        stream.getTracks().forEach(track => track.stop());
        video.srcObject = null;
        await progressUpdate();
    }

    async function takePicture() {
        try {
            const canvas = document.createElement('canvas');
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;

            const context = canvas.getContext('2d');
            context.drawImage(video, 0, 0, canvas.width, canvas.height);

            const data = await new Promise((resolve) => {
                canvas.toBlob((blob) => {
                    resolve(blob);
                }, 'image/png', 1);
            });

            const formData = new FormData();
            formData.append('image', data);
            formData.append('number', number);

            const token = localStorage.getItem('token')

            const response = await axios.post(
                PUBLIC_API_URL + '/image_handle',
                formData,
                {
                    headers: {
                        'Content-Type': 'multipart/form-data',
                        'Access-Control-Allow-Origin': "*",
                        'token': `Bearer ${token}`
                    },
                }
            );
            if (response) {
                const data = response.data;
                const imageUrl = data.image;
                counter = data.counter;
                photo.setAttribute("src", imageUrl);
            } else {
                console.error('Image upload failed.');
            }

            if(counter == 100) {
                progressValue += 5;
                i++;
                number = numbers[i];
                notifications.success('Правильно!', 5000)
            } else(
                notifications.danger('Жест показан неправильно! Попробуйте еще раз!', 5000)
            )


        } catch (error) {
            console.error(error);
        }
    }

    async function getProgress() {
        const token = localStorage.getItem('token')

        const config = {
            headers: {
                'Content-Type': 'application/json',
                'token': `Bearer ${token}`
            }
        };

        try {
            const response = await axios.post(PUBLIC_API_URL + '/get_progress', { lesson_id }, config);
            const result = response.data;
            progressValue = result.progress;
            console.log(result.progress)
        } catch (error) {
            console.error(error);
        }
    }

    onMount(getProgress);

</script>

<main>
    <div>
        <h1>{lesson[0].name}</h1>
    </div>
    <div>
        <p>{lesson[0].content}</p>
    </div>

    <div>
        {#if level_id === 1}
            {#if lesson_id === 1}
                <img src={Image11} alt="image">
            {/if}
            {#if lesson_id === 2}
                <img src={Image12} alt="image">
            {/if}
        {/if}
        {#if level_id === 2}
            {#if lesson_id === 3}
                <img src={Image21} alt="image">
            {/if}
            {#if lesson_id === 4}
                <img src={Image22} alt="image">
            {/if}
            {#if lesson_id === 5}
                <img src={Image23} alt="image">
            {/if}
            {#if lesson_id === 6}
                <img src={Image24} alt="image">
            {/if}
            {#if lesson_id === 7}
                <img src={Image25} alt="image">
            {/if}
        {/if}
    </div>

    <div class="contentarea">
        <h1>Практика</h1>
        <p>Для начала тренировки нажмите "Начать".</p>
        {#if level_id === 1}
            <p>Покажите жестом цифру {number}, расположите жест внутри синей рамки</p>
        {/if}

        {#if level_id === 2}
            <p>Покажите жестом букву {letters_map[number]}, расположите жест внутри синей рамки</p>
        {/if}

        <div id="videoContainer">
            <video id="video" width="320" height="240" autoplay></video>
            <canvas id="canvas" width="320" height="240"></canvas>
            <button id="startbutton" on:click={takePicture}>Проверить</button>
        </div>

        <div class="output"><img id="photo"/></div>
        <div>
            <button on:click={getStream}>Начать</button>
            <button on:click={stopStream}>Остановить</button>
        </div>
    </div>
    <Toast />

    <h3>Ваш прогресс по уроку {progressValue}%</h3>>
    <div>
        <progress max="100" value="{progressValue}"></progress>
    </div>
</main>


<style>
    #videoContainer {
        position: relative;
        display: inline-block;
        width: 340px;
    }

    #canvas {
        position: absolute;
        top: 0;
        left: 0;
    }

    h1{
        text-align: center;
        color: #333333;
        font-family: var(--font-mono);
    }

    p {
        text-align: center;
        color: #333333;
        font-family: var(--font-mono);
        font-size: large;
        font-weight: bold;
    }
    #video {
        border: 1px solid black;
        box-shadow: 10px 5px 5px black;
        width: 320px;
        height: 240px;
        position: relative;
        display: inline-block;
    }

    #photo {
        border: 1px solid black;
        box-shadow: 10px 5px 5px black;
        width: 320px;
        height: 240px;
    }

    .output {
        width: 340px;
        display: inline-block;
        vertical-align: top;
    }

    button {
        color: #ffffff;
        background-color: rgb(75, 110, 255);
    }

    #startbutton {
        display: block;
        position: relative;
        margin-left: auto;
        margin-right: auto;
        bottom: 32px;
        background-color: rgb(75, 110, 255);
        border: 1px solid rgba(255, 255, 255, 0.7);
        box-shadow: 0px 0px 1px 2px rgba(0, 0, 0, 0.2);
        font-size: 14px;
        font-family: "Lucida Grande", "Arial", sans-serif;
        color: rgba(255, 255, 255, 1);
    }

    .contentarea {
        font-size: 16px;
        font-family: "Lucida Grande", "Arial", sans-serif;
        width: 100%;
    }


    h3 {
        text-align: initial;
        color: #333333;
    }

    img {
        display: block;
        margin: 0 auto;
    }

</style>