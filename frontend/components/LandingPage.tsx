"use client";
import getQuest from "@/lib/api";
import { useState } from "react";

export default function LandingPage() {
  const [time, setTime] = useState<number | null>(null);

  return (
    <div className="flex flex-col items-center justify-center h-screen">
      <div className="flex items-center gap-2">
        <h1>I have</h1>
        <input
          className="border-2 border-gray-300 rounded-md p-1 w-16 step={15}:"
          type="number"
          value={time ?? ""}
          step={15}
          
          onChange={(e) =>
            setTime(e.target.value === "" ? null : Number(e.target.value))
          }
        />
        <h1>minutes</h1>
      </div>

      <button 
        onClick={() => getQuest(time ?? 0)}
        className="mt-4 rounded-md bg-blue-500 px-4 py-2 text-white hover:bg-blue-600 cursor-pointer click:bg-blue-700">
        Find Me Something To Do
      </button>
    </div>
  );
}