const getQuest = async (time: number) => {
    const response = await fetch(`${process.env.BACKEND_API_URL}/quests?time=${time}`);
    const data = await response.json();
    return data;
}

export default getQuest;