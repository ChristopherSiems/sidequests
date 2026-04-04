import { Quest } from "@/interfaces/interfaces";
import QuestCard from "./QuestCard";
import { useSwipeable } from "react-swipeable";
import { isMobile } from "@/lib/utils";
import { useState } from "react";
import ExpandedQuestCard from "./ExpandedQuestCard";
interface QuestPageProps {
  setOnLanding: (onLanding: boolean) => void;
  quest: Quest | null;
  getNewQuest: () => void;
}
export default function QuestPage({
  setOnLanding,
  quest,
  getNewQuest,
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
  return (
    <div {...handlers} className="flex flex-col items-center justify-center h-screen">
      <button onClick={() => setOnLanding(true)}>Back</button>
      <div className="flex items-center justify-center gap-4">
        {!isMobileEnv && (
          <button
            className="cursor-pointer hover:bg-blue-500 hover:text-white rounded-md px-4 py-2"
            onClick={() => swipeLeft()}
          >
            New Quest
          </button>
        )}
        {quest && (expandedQuest ? <ExpandedQuestCard quest={quest} /> : <QuestCard quest={quest} />)}
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
  );
}
