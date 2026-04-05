import { EmbeddingHistory } from "@/interfaces/interfaces";
import axios from "axios";

const BASE_URL = process.env.NEXT_PUBLIC_BACKEND_API_URL;
const getQuest = async (time: number, location: [number, number], embeddingHistory: EmbeddingHistory[]) => {
    console.log(BASE_URL);
    try{
        const body = {
            "minutes": time, 
            "location": location,
            "embedding_history": embeddingHistory
        }
        const response =  await axios.post(`${BASE_URL}/quest`, body);
        const data = response.data;
        console.log('data', data);
        return data;
    } catch (error) {
        console.error(error);
        return null;
    }
}

const addInteraction = async (embedding: number[], score: number) => {
    console.log(embedding, score);
    try {
        const body = {
            "embedding": embedding,
            "score": score
        }
        await axios.post(`${BASE_URL}/interactions`, body);
    }
    catch (error) {
        console.error(error);
    }
}

export { getQuest, addInteraction };

