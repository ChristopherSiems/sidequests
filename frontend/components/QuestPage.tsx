import { Quest } from "@/interfaces/interfaces";
import QuestCard from "./QuestCard";
import { useSwipeable } from "react-swipeable";
import { isMobile } from "@/lib/utils";
import { useState } from "react";
import ExpandedQuestCard from "./ExpandedQuestCard";
import { DirectionsMap } from "./DirectionsMap";
import QuestHeader from "./QuestHeader";
import { addInteraction } from "@/lib/api";
import { useLocalStorage } from 'usehooks-ts'
import { EmbeddingHistory } from "@/interfaces/interfaces";
interface QuestPageProps {
  setOnLanding: (onLanding: boolean) => void;
  quest: Quest | null;
  getNewQuest: (historyOverride?: EmbeddingHistory[]) => void | Promise<void>;
  time: number;
  setTime: (time: (currentTime: number) => number) => void;
  location: [number, number];
  embeddingHistory: EmbeddingHistory[];
  setEmbeddingHistory: (embeddingHistory: EmbeddingHistory[]) => void;
}

export default function QuestPage({
  quest,
  getNewQuest,
  time,
  setTime,
  location,
  embeddingHistory,
  setEmbeddingHistory,
}: QuestPageProps) {
  const [expandedQuest, setExpandedQuest] = useState<boolean>(false);


  const swipeLeft = () => {
    setExpandedQuest(false);
    const entry = { embedding: quest?.embedding || [], score: -1 };
    const nextHistory = [...embeddingHistory, entry];
    setEmbeddingHistory(nextHistory);
    if (quest?.embedding && quest?.embedding.length > 0){
        setEmbeddingHistory([...embeddingHistory, { embedding: quest.embedding, score: -1 }])
    }
    void getNewQuest(nextHistory);
  };

  const swipeRight = () => {
    console.log("right");
    setExpandedQuest(true);
    addInteraction(quest?.embedding || [], 1);
    if (quest?.embedding && quest?.embedding.length > 0){
        setEmbeddingHistory([...embeddingHistory, { embedding: quest.embedding, score: 1 }])
    }
   
  };
  const handlers = useSwipeable({
    onSwipedLeft: swipeLeft,
    onSwipedRight: swipeRight,
    trackMouse: true
  });
  
    const directionsMap = <DirectionsMap userLat={location[0]} userLng={location[1]} destination={quest?.location || ""} />;
  const displayExpandedCard =  expandedQuest? "" : "none"
  return (
    <div className="flex min-h-0 flex-col items-center h-screen">
        <QuestHeader time={time} setTime={setTime} />
   
    <div {...handlers} className="flex min-h-0 w-full flex-1 flex-col items-center justify-center">
      
      {/* <button onClick={() => setOnLanding(true)}>Back</button> */}
      <div className="flex items-center justify-center gap-4">

        {!quest && <h2>No Activities Found</h2>}
        {quest && !expandedQuest && <QuestCard quest={quest} />}
        <div style={{ display: displayExpandedCard }}>
        {quest && quest.location && <ExpandedQuestCard quest={quest} directionsMap={directionsMap} />}
        </div>
        
      </div>
    
    </div>
        <h2 className="text-center text-sm mt-6 text-gray-500 pb-8" >Swipe left to get a new quest, swipe right to see the current quest</h2>
    </div>
  );
}
