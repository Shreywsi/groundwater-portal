import { useEffect, useState } from "react";
import axios from "axios";

import {
  Container,
  Typography,
  Box,
  ToggleButton,
  ToggleButtonGroup,
  CircularProgress,
  Alert,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
} from "@mui/material";

import { getForecast } from "../../services/forecastApi";

import AIPredictionCard from "../../components/admin/AIPredictionCard";

export default function AIPrediction() {

  const [period, setPeriod] = useState("monthly");

  const [forecast, setForecast] = useState(null);

  const [loading, setLoading] = useState(false);

  const [error, setError] = useState("");

  const [locations, setLocations] = useState([]);

  const [selectedLocation, setSelectedLocation] = useState("");

  useEffect(() => {

    axios
      .get("http://127.0.0.1:8000/api/location-list/")
      .then((res) => {

        setLocations(res.data);

        if (res.data.length > 0) {

          setSelectedLocation(res.data[0].id);

        }

      });

  }, []);

  useEffect(() => {

    if (selectedLocation) {

      loadForecast(period, selectedLocation);

    }

  }, [period, selectedLocation]);

  async function loadForecast(selectedPeriod, location) {

    try {

      setLoading(true);

      setError("");

      const data = await getForecast(
        selectedPeriod,
        location
      );

      setForecast(data);

    }

    catch (err) {

      setError(err.message);

    }

    finally {

      setLoading(false);

    }

  }

  return (

    <Container maxWidth="xl">

      <Typography
        variant="h4"
        fontWeight="bold"
        sx={{ mb: 3 }}
      >
        AI Water Balance Forecasting
      </Typography>

      <FormControl
        fullWidth
        sx={{ mb: 3 }}
      >

        <InputLabel>

          Location

        </InputLabel>

        <Select

          value={selectedLocation}

          label="Location"

          onChange={(e) => {

            setSelectedLocation(e.target.value);

          }}

        >

          {locations.map((location) => (

            <MenuItem
              key={location.id}
              value={location.id}
            >

              {location.name}

            </MenuItem>

          ))}

        </Select>

      </FormControl>

      <ToggleButtonGroup

        exclusive

        value={period}

        onChange={(e, value) => {

          if (value) {

            setPeriod(value);

          }

        }}

        sx={{ mb: 4 }}

      >

        <ToggleButton value="monthly">
          Monthly
        </ToggleButton>

        <ToggleButton value="quarterly">
          Quarterly
        </ToggleButton>

        <ToggleButton value="halfyearly">
          Half-Yearly
        </ToggleButton>

        <ToggleButton value="annual">
          Annual
        </ToggleButton>

        <ToggleButton value="10years">
          10 Years
        </ToggleButton>

        <ToggleButton value="30years">
          30 Years
        </ToggleButton>

      </ToggleButtonGroup>

      {loading && (

        <Box mt={5}>

          <CircularProgress />

        </Box>

      )}

      {error && (

        <Alert severity="error">

          {error}

        </Alert>

      )}

      {!loading &&
        !error &&
        forecast && (

          <AIPredictionCard
            data={forecast}
          />

      )}

    </Container>

  );

}