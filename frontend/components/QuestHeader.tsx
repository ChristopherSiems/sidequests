import { GoTriangleDown, GoTriangleUp } from "react-icons/go";

interface QuestHeaderProps {
    time: number;
    setTime: (time: (currentTime: number) => number) => void;
}
export default function QuestHeader({time, setTime}: QuestHeaderProps) {
    return (
        <div className="flex flex-col items-center justify-center pt-12">
      <div className="flex items-center gap-2">
        <h1 className="text-xl font-bold">Showing activities for</h1>
        
        <div className="flex flex-col items-center">
          <GoTriangleUp
            size={60}
            className="cursor-pointer"
            onClick={() =>
              setTime((currentTime) => currentTime + 15)
            }
          />

          <input
            className="border-2 border-gray-300 rounded-md p-1 w-16 text-center"
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
        <h1 className="text-xl font-bold">minutes</h1>
      </div>

    </div>
    )
}