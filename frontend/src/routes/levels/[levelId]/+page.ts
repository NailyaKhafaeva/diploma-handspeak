import {
    PUBLIC_API_URL
} from "$env/static/public";
// @ts-ignore
export const load = ({ fetch, params}) => {

    // @ts-ignore
    const fetchLessons = async (levelId) => {
        const token = localStorage.getItem('token')
        const config = {
            headers: {
                'Content-Type': 'application/json',
                'token': `Bearer ${token}`
            }
        };

        const res = await fetch(PUBLIC_API_URL + `/get_lessons/${levelId}`, config)
        const data = await res.json()
        return data
    }

    return {
        lessons: fetchLessons(params.levelId)
    }
}