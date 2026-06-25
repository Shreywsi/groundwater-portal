import {
  MapContainer,
  TileLayer,
  Marker,
  Popup,
  Polygon,
} from "react-leaflet";

import "leaflet/dist/leaflet.css";

const wells = [
  {
    id: 1,
    name: "Well A",
    position: [23.2451, 69.6661],
    waterLevel: 12,
  },
  {
    id: 2,
    name: "Well B",
    position: [23.265, 69.69],
    waterLevel: 18,
  },
];

const pondCoordinates = [
  [23.23, 69.62],
  [23.235, 69.62],
  [23.235, 69.635],
  [23.23, 69.635],
];

const farmCoordinates = [
  [23.27, 69.72],
  [23.28, 69.72],
  [23.28, 69.74],
  [23.27, 69.74],
];

export default function WaterMap() {
  return (
    <MapContainer
      center={[23.25, 69.68]}
      zoom={9}
      style={{
        height: "500px",
        width: "100%",
        borderRadius: "8px",
      }}
    >
      <TileLayer
        attribution="&copy; OpenStreetMap contributors"
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />

      {/* Wells */}
      {wells.map((well) => (
        <Marker key={well.id} position={well.position}>
          <Popup>
            <strong>{well.name}</strong>
            <br />
            Water Level: {well.waterLevel} m
          </Popup>
        </Marker>
      ))}

      {/* Pond */}
      <Polygon
        positions={pondCoordinates}
        pathOptions={{
          color: "blue",
          fillColor: "lightblue",
          fillOpacity: 0.6,
        }}
      >
        <Popup>
          <strong>Pond</strong>
          <br />
          Sample Water Body
        </Popup>
      </Polygon>

      {/* Farm */}
      <Polygon
        positions={farmCoordinates}
        pathOptions={{
          color: "green",
          fillColor: "green",
          fillOpacity: 0.4,
        }}
      >
        <Popup>
          <strong>Farm Plot</strong>
          <br />
          Sample Agricultural Area
        </Popup>
      </Polygon>
    </MapContainer>
  );
}