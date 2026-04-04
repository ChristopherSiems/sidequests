import { Quest } from "@/interfaces/interfaces";
import { formatTime } from "@/lib/utils";
interface ExpandedQuestCardProps {
    quest: Quest;
}
export default function ExpandedQuestCard({quest}: ExpandedQuestCardProps) {
    return (
        <div className="flex flex-col items-center justify-center border-2 border-gray-300 rounded-md p-4 w-[300px] h-[500px]">
            <h1>{quest.title}</h1>
            <h1>{formatTime(quest.end_time - quest.start_time)}</h1>
            
        </div> 
        
    )
}