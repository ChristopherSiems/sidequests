import { Quest } from "@/interfaces/interfaces";

interface QuestCardProps {
    quest: Quest;
}
export default function QuestCard({quest}: QuestCardProps) {
    return (
        <div className="flex flex-col items-center justify-center border-2 border-gray-300 rounded-md p-4 w-[300px] h-[200px]">
            <h2>{quest.title}</h2>
        </div>  
    )
}

