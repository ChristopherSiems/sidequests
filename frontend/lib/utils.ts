const getDisplayTime = (time: number) => {
    if (time < 60) {
        return time
    }
    if (time == 60) {
        return 1; 
    } 
    if (time > 60) {
        return Math.round(time / 60 * 4) / 4; 
    }
    return time;
}

const formatTime = (seconds: number): string => {

    const totalMinutes = Math.round(seconds / 60);
  
    const hours = Math.floor(totalMinutes / 60);
    const minutes = totalMinutes % 60;
  
    let result = "";
    if (hours > 0) result += `${hours} ${hours === 1 ? "hour" : "hours"}`;
    if (minutes > 0) {
      if (hours > 0) result += " ";
      result += `${minutes} ${minutes === 1 ? "minute" : "minutes"}`;
    }
    if (result === "") return "0 minutes"; 
  
    return result;
  };
const isMobile = () => {
    return /Android|iPhone|iPad|iPod|Opera Mini|IEMobile|WPDesktop/i.test(navigator.userAgent);
}
export { getDisplayTime, isMobile, formatTime };


