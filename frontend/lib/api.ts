import axios from "axios";

const getQuest = async (time: number, location: [number, number]) => {
    try{
        const body = {
            "time": time, 
            "location": location
        }
        const response =  await axios.post(`${process.env.BACKEND_API_URL}/quests`, body);
        const data = response.data;
        return data;
    } catch (error) {
        console.error(error);
        return [];
    }
}

export default getQuest;