interface DirectionsMapProps {
    userLat: number;
    userLng: number;
    destination: string
  }
  
  export const DirectionsMap = ({ userLat, userLng }: DirectionsMapProps) => {
    const destination = { lat: 34.0522, lng: -118.2437 }; // Los Angeles, CA
    const apiKey = process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY;
  
    const url = `https://www.google.com/maps/embed/v1/directions?key=${apiKey}&origin=${userLat},${userLng}&destination=${destination}}`;
  
    return (
      <iframe
        title="Google Maps Directions"
        width="100%"
        height="450"
        style={{ border: 0 }}
        loading="lazy"
        allowFullScreen
        src={url}
      />
    );
  };