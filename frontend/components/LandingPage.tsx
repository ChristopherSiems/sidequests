"use client";
import { GoTriangleUp, GoTriangleDown } from "react-icons/go";

interface LandingPageProps {
  time: number;
  setTime: (time: (currentTime: number) => number) => void;
  setOnLanding: (onLanding: boolean) => void;
  getNewQuest: () => void;
}

export default function LandingPage({
  time,
  setTime,
  setOnLanding,
  getNewQuest,
}: LandingPageProps) {
  const handleFind = async () => {
    getNewQuest();
    setOnLanding(false);
  };

  return (
    <div className="flex flex-col items-center justify-center h-screen">
      <div className="flex items-center gap-3">
        <h1>I have</h1>

        <div className="flex flex-col items-center">
          <GoTriangleUp
            size={60}
            className="cursor-pointer"
            onClick={() =>
              setTime((currentTime) => currentTime + 15)
            }
          />

          <input
            className="border-2 border-gray-300 rounded-md pl-1 pr-1 w-16 text-center"
            type="number"
            value={time}
            step={15}
            min={0}
            onChange={(e) =>
              setTime(() =>
                e.target.value === "" ? 0 : Number(e.target.value)
              )
            }
          />

          <GoTriangleDown
            size={60}
            className="cursor-pointer"
            onClick={() =>
              setTime((currentTime) => Math.max(0, currentTime - 15))
            }
          />
        </div>

        <h1>minutes</h1>
      </div>

      <button
        onClick={handleFind}
        className="mt-4 rounded-md bg-blue-500 px-4 py-2 text-white hover:bg-blue-600 cursor-pointer active:bg-blue-700"
      >
        Find Me Something To Do
      </button>
    </div>
  );
}