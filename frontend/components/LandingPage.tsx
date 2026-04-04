"use client";

interface LandingPageProps {
    time: number;
    setTime: (time: number) => void;
    setOnLanding: (onLanding: boolean) => void;
    getNewQuest: () => void;
}
export default function LandingPage({time, setTime, setOnLanding, getNewQuest}: LandingPageProps) {
    const handleFind = async () => {
        getNewQuest();
        setOnLanding(false);
    }
  return (
    <div className="flex flex-col items-center justify-center h-screen">
      <div className="flex items-center gap-2">
        <h1>I have</h1>
        <input
          className="border-2 border-gray-300 rounded-md p-1 w-16 step={15}:"
          type="number"
          value={time}
          step={15}
          min={0}
          onChange={(e) =>
            setTime(e.target.value === "" ? 0: Number(e.target.value))
          }
        />
        <h1>minutes</h1>
      </div>

      <button 
        onClick={handleFind}
        className="mt-4 rounded-md bg-blue-500 px-4 py-2 text-white hover:bg-blue-600 cursor-pointer click:bg-blue-700">
        Find Me Something To Do
      </button>
    </div>
  );
}