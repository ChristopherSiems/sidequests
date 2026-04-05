"use client";
import LandingPage from "@/components/LandingPage";
import QuestPage from "@/components/QuestPage";
import { Quest } from "@/interfaces/interfaces";
import getQuest from "@/lib/api";
import { useState } from "react";

export default function Home() {
  const [quest, setQuest] = useState<Quest | null>(null);
  const [onLanding, setOnLanding] = useState<boolean>(true);
  const [time, setTime] = useState<number>(0);
  const getNewQuest = async () => {
    const newQuest = await getQuest(time, [0, 0]);
    setQuest(newQuest);
  }
  return onLanding ? (
      <LandingPage
        time={time}
        setTime={setTime}
        setOnLanding={setOnLanding}
        getNewQuest={getNewQuest}
      />
  ) : (
      <QuestPage setOnLanding={setOnLanding} quest={quest} getNewQuest={getNewQuest} time={time} setTime={setTime} />
    );
}
