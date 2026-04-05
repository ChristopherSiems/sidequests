interface DirectionsMapProps {
    userLat: number;
    userLng: number;
    destination: string
  }
  
  export const DirectionsMap = ({ userLat, userLng ,destination}: DirectionsMapProps) => {
    const apiKey = process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY;
    console.log(userLat, userLng, destination);
  
    const url = `https://www.google.com/maps/embed/v1/directions?key=${apiKey}&origin=${userLat},${userLng}&destination=${destination}&mode=walking`;
  
    return (
      <iframe
        title="Google Maps Directions"
        width="100%"
        height="400"
        style={{ border: 0 }}
        loading="eager"
        allowFullScreen
        src={url}
      />
    );
  };