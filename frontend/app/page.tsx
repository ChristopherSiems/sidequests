"use client";
import LandingPage from "@/components/LandingPage";
import QuestPage from "@/components/QuestPage";
import { EmbeddingHistory, Quest } from "@/interfaces/interfaces";
import { getQuest } from "@/lib/api";
import { useState } from "react";
import { useLocation } from "./hooks/hooks";
import { useLocalStorage } from "usehooks-ts";

export default function Home() {
  const [quest, setQuest] = useState<Quest | null>(null);
  const [onLanding, setOnLanding] = useState<boolean>(true);
  const [time, setTime] = useState<number>(15);
  const userLocation = useLocation();
  const [embeddingHistory, setEmbeddingHistory] = useLocalStorage<EmbeddingHistory[]>(
    "embeddingHistory",
    []
  );
  const getNewQuest = async (historyForRequest?: EmbeddingHistory[]) => {
    const history = historyForRequest ?? embeddingHistory;
    const newQuest = await getQuest(time, userLocation, history);
    setQuest(newQuest);
  };
  return onLanding ? (
      <LandingPage
        time={time}
        setTime={setTime}
        setOnLanding={setOnLanding}
        getNewQuest={getNewQuest}
      />
  ) : (
      <QuestPage setOnLanding={setOnLanding} quest={quest} getNewQuest={getNewQuest} time={time} setTime={setTime} location={userLocation} embeddingHistory={embeddingHistory} setEmbeddingHistory={setEmbeddingHistory}  />
    );
}
