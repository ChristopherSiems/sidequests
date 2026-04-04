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

export default getDisplayTime;
