import { useEffect, useState } from "react";

import {
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Container,
  Typography,
  Box,
  ToggleButton,
  ToggleButtonGroup,
  CircularProgress,
  Alert,
} from "@mui/material";

import { getForecast } from "../../services/forecastApi";

import AIPredictionCard from "../../components/admin/AIPredictionCard";

export default function AIPrediction() {

  const [period, setPeriod] = useState("monthly");
  const [location, setLocation] = useState(6);
  const [forecast, setForecast] = useState(null);

  const [loading, setLoading] = useState(false);

  const [error, setError] = useState("");

  useEffect(() => {
      loadForecast(period, location);
  }, [period, location]);

  async function loadForecast(selectedPeriod, selectedLocation) {

    try {

      setLoading(true);

      setError("");

      const data = await getForecast(
        selectedPeriod,
        selectedLocation
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
    sx={{ minWidth: 250, mb: 3 }}
>

    <InputLabel>
        Location
    </InputLabel>

    <Select
        value={location}
        label="Location"
        onChange={(e) =>
            setLocation(e.target.value)
        }
    >

        <MenuItem value={5}>
            Mundra
        </MenuItem>

        <MenuItem value={6}>
            Abdasa
        </MenuItem>

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