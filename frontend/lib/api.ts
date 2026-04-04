import axios from "axios";
const BASE_URL = process.env.NEXT_PUBLIC_BACKEND_API_URL;
const getQuest = async (time: number, location: [number, number]) => {
    console.log(BASE_URL);
    try{
        const body = {
            "time": time, 
            "location": location
        }
        const response =  await axios.post(`${BASE_URL}/quest`, body);
        const data = response.data;
        return data;
    } catch (error) {
        console.error(error);
        return [];
    }
}

export default getQuest;