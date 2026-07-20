import { useState, useEffect } from "react";
import axios from "axios";

import {
  Card,
  Typography,
  TextField,
  Button,
  List,
  ListItem,
  ListItemText,
  Stack,
  Alert,
  CircularProgress,
} from "@mui/material";

export default function Locations() {
  const [name, setName] = useState("");
  const [locations, setLocations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  const loadLocations = async () => {
    try {
      const res = await axios.get(
        "http://127.0.0.1:8000/api/location-list/"
      );
      setLocations(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    loadLocations();
  }, []);

  const addLocation = async () => {
    if (!name.trim()) return;

    setLoading(true);
    setMessage("");

    try {
      // Validate location using OpenStreetMap
      const geo = await axios.get(
        "https://nominatim.openstreetmap.org/search",
        {
          params: {
            q: name,
            format: "json",
            limit: 1,
          },
          headers: {
            Accept: "application/json",
          },
        }
      );

      if (geo.data.length === 0) {
        setMessage("Invalid location. Please enter a real location.");
        setLoading(false);
        return;
      }

      const place = geo.data[0];

      await axios.post(
        "http://127.0.0.1:8000/api/location/add/",
        {
          name: place.display_name,
          location_type: "Location",
          district: "",
          state: "",
        }
      );

      setName("");
      loadLocations();
      setMessage("Location added successfully.");
    } catch (err) {
      console.error(err);
      setMessage("Something went wrong.");
    }

    setLoading(false);
  };

  return (
    <Card sx={{ p: 4 }}>
      <Typography variant="h5" gutterBottom>
        Manage Locations
      </Typography>

      {message && (
        <Alert sx={{ mb: 2 }}>
          {message}
        </Alert>
      )}

      <Stack direction="row" spacing={2} sx={{ mb: 3 }}>
        <TextField
          fullWidth
          label="Enter Location"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />

        <Button
          variant="contained"
          disabled={loading}
          onClick={addLocation}
        >
          {loading ? (
            <CircularProgress size={22} color="inherit" />
          ) : (
            "Add"
          )}
        </Button>
      </Stack>

      <List>
        {locations.map((location) => (
          <ListItem key={location.id}>
            <ListItemText
              primary={location.name}
              secondary={location.location_type}
            />
          </ListItem>
        ))}
      </List>
    </Card>
  );
}