import { Quest } from "@/interfaces/interfaces";
import QuestCard from "./QuestCard";
import { useSwipeable } from "react-swipeable";
import { isMobile } from "@/lib/utils";
import { useState } from "react";
import ExpandedQuestCard from "./ExpandedQuestCard";
import { DirectionsMap } from "./DirectionsMap";
import QuestHeader from "./QuestHeader";
interface QuestPageProps {
  setOnLanding: (onLanding: boolean) => void;
  quest: Quest | null;
  getNewQuest: () => void;
  time: number;
  setTime: (time: number) => void;
  location: [number, number];
}
export default function QuestPage({
  quest,
  getNewQuest,
  time,
  setTime,
  location,
}: QuestPageProps) {
  const [expandedQuest, setExpandedQuest] = useState<boolean>(false);
  const swipeLeft = () => {
    getNewQuest();
    setExpandedQuest(false);
  };
  const swipeRight = () => {
    console.log("right");
    setExpandedQuest(true);
  };
  const handlers = useSwipeable({
    onSwipedLeft: swipeLeft,
    onSwipedRight: swipeRight,
    trackMouse: true
  });
  
  const isMobileEnv = isMobile();
  
  const directionsMap = <DirectionsMap userLat={location[0]} userLng={location[1]} destination={quest?.location || ""} />;
  const displayExpandedCard =  expandedQuest? "" : "none"
  return (
    <div className="flex flex-col items-center  h-screen">
        <QuestHeader time={time} setTime={setTime} />
   
    <div {...handlers} className="flex flex-col items-center justify-center h-full">
      
      {/* <button onClick={() => setOnLanding(true)}>Back</button> */}
      <div className="flex items-center justify-center gap-4">
        {!isMobileEnv && (
          <button
            className="cursor-pointer hover:bg-blue-500 hover:text-white rounded-md px-4 py-2"
            onClick={() => swipeLeft()}
          >
            New Quest
          </button>
        )}
        
        {quest && !expandedQuest && <QuestCard quest={quest} />}
        <div style={{ display: displayExpandedCard }}>
        {quest && <ExpandedQuestCard quest={quest} directionsMap={directionsMap} />}
        </div>
        {!isMobileEnv? !expandedQuest? (
          <button
            className="cursor-pointer hover:bg-blue-500 hover:text-white rounded-md px-4 py-2 w-[100px]"
            onClick={() => swipeRight()}
          >
            Explore Quest
          </button>
        ) : <div className="w-[100px]"></div>: <> </>}
      </div>
    
    </div>
    {isMobileEnv && <h2 className="text-center text-sm mt-6 text-gray-500 pb-2" >Swipe left to get a new quest, swipe right to see the current quest</h2>}
    </div>
  );
}
