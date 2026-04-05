import { Quest } from "@/interfaces/interfaces";
import { formatTime } from "@/lib/utils";
import { DirectionsMap } from "./DirectionsMap";
interface ExpandedQuestCardProps {
    quest: Quest;
    directionsMap: React.ReactNode;
}
export default function ExpandedQuestCard({quest, directionsMap}: ExpandedQuestCardProps) {
    return (
        <div className="flex flex-col items-center justify-center border-2 border-gray-300 rounded-md p-4 w-[300px] h-[500px]">
            <h1 className="text-xl font-bold text-center mb-2">{quest.title}</h1>
            {directionsMap}
            <h1 className="mt-2">Event Duration: {quest.end_time ? formatTime(quest.end_time - quest.start_time ) : "Open All Day"}</h1>
            {quest.link && <a href = {quest.link} className="w-[200px] text-center p-2 rounded-md text-white gray-500 mt-2"> View External Source</a>}
            
        </div> 

    )
}