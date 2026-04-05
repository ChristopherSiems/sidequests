import { useState, useEffect } from "react";



export function useLocation(): [number, number] {
  const [location, setLocation] = useState<[number, number]>([0, 0]);

  useEffect(() => {
    if (!navigator.geolocation) {
      setLocation([0, 0]);
      return;
    }

    const success = (position: GeolocationPosition) => {
      setLocation([position.coords.latitude, position.coords.longitude]);
    };

    const error = (err: GeolocationPositionError) => {
        setLocation([0, 0]);
        console.error(err);
    };

    const watcher = navigator.geolocation.watchPosition(success, error);

    // Cleanup
    return () => {
      navigator.geolocation.clearWatch(watcher);
    };
  }, []);

  return location;
}