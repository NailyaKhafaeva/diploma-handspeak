import {
    PUBLIC_API_URL
} from "$env/static/public";
// @ts-ignore
export const load = async ({ fetch }) => {

    const fetchLevels = async () => {
        const token = localStorage.getItem('token')
        const config = {
            headers: {
                'Content-Type': 'application/json',
                'token': `Bearer ${token}`
            }
        };

        const levelRes = await fetch(PUBLIC_API_URL + '/get_levels', config)
        const levelData = await levelRes.json()
        return levelData.levels
    }

    return {
        levels: fetchLevels(),
    }
}