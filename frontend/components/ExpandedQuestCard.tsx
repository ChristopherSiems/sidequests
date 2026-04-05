import { Quest } from "@/interfaces/interfaces";
import { formatTime } from "@/lib/utils";
import { DirectionsMap } from "./DirectionsMap";
interface ExpandedQuestCardProps {
    quest: Quest;
    directionsMap: React.ReactNode;
}
export default function ExpandedQuestCard({quest, directionsMap}: ExpandedQuestCardProps) {
    const duration =(quest.end_time - quest.start_time) //<  100 * 60 * 60 ? (quest.end_time - quest.start_time) : 120*60;
    // const timeRemaining   /= Math.min(duration, quest.end_time - Date.now()/1000);
    console.log("quest", quest, duration);
    return (
        <div className="flex flex-col items-center justify-center border-2 border-gray-300 rounded-md p-4 w-[300px] h-[500px]">
            <h1 className="text-xl font-bold text-center mb-2">{quest.title}</h1>
            {directionsMap}<h1 className="mt-2">{quest.end_time === "string" ? "Time:" : "Duration:"} {typeof quest.end_time === "number" ? formatTime(duration ) :typeof quest.end_time === "string" ? quest.start_time + " to " + quest.end_time : "Open All Day"}</h1>
            {quest.link && <a href = {quest.link} target="_blank" className="w-[200px] text-center p-2 rounded-md text-white  bg-gray-500 mt-2"> View External Source</a>}
            
        </div> 

    )
}