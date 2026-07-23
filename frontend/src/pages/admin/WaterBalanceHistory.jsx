import { useEffect, useState } from "react";
import axios from "axios";
import API_BASE from "../../config/api";
import Sidebar from "../../components/Sidebar";
import {
  Card,
  Typography,
  Table,
  TableHead,
  TableRow,
  TableCell,
  TableBody,
  TableContainer,
  Chip,
  Grid,
  TextField,
  Paper,
  Box,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
} from "@mui/material";

export default function WaterBalanceHistory() {
  const [history, setHistory] = useState([]);
  const [summary, setSummary] = useState({});
  const [search, setSearch] = useState("");
  const [locations, setLocations] = useState([]);
  const [selectedLocation, setSelectedLocation] = useState("");

  // Load list of locations once, on page load
  useEffect(() => {
    const loadLocations = async () => {
      try {
        const res = await axios.get(`${API_BASE}/location-list/`);
        setLocations(res.data);
        if (res.data.length > 0) {
          setSelectedLocation(res.data[0].id);
        }
      } catch (err) {
        console.error(err);
      }
    };
    loadLocations();
  }, []);

  // Reload history whenever the selected location changes
  useEffect(() => {
    if (selectedLocation) {
      loadHistory(selectedLocation);
    }
  }, [selectedLocation]);

  const loadHistory = async (locationId) => {
    try {
      const res = await axios.get(`${API_BASE}/water-balance/history/`, {
        params: { location: locationId },
      });

      setHistory(res.data.records);
      setSummary(res.data.summary);
    } catch (err) {
      console.error(err);
      setHistory([]);
      setSummary({});
    }
  };

  const filteredHistory = history.filter((item) =>
  `${item.date} ${item.time}`
    .toLowerCase()
    .includes(search.toLowerCase())
);

  return (
    <Box sx={{ display: "flex", minHeight: "100vh" }}>

        <Sidebar />

        <Box
        sx={{
            flex: 1,
            p: 3,
            bgcolor: "#f5f7fb",
        }}
        >

      <Typography variant="h4" fontWeight="bold" gutterBottom>
        Water Balance History
      </Typography>

      {/* LOCATION SELECTOR */}
      <FormControl sx={{ minWidth: 250, mb: 3 }}>
        <InputLabel>Location</InputLabel>
        <Select
          value={selectedLocation}
          label="Location"
          onChange={(e) => setSelectedLocation(e.target.value)}
        >
          {locations.length === 0 ? (
            <MenuItem disabled>No Locations Found</MenuItem>
          ) : (
            locations.map((loc) => (
              <MenuItem key={loc.id} value={loc.id}>
                {loc.name}
              </MenuItem>
            ))
          )}
        </Select>
      </FormControl>

      {/* SUMMARY CARDS */}

      <Grid container spacing={2} sx={{ mb: 3 }}>

        <Grid item xs={12} md={3}>
          <Paper sx={{ p: 2 }}>
            <Typography color="text.secondary">
              Total Records
            </Typography>

            <Typography variant="h4">
              {summary.total_records ?? 0}
            </Typography>
          </Paper>
        </Grid>

        <Grid item xs={12} md={3}>
          <Paper sx={{ p: 2 }}>
            <Typography color="text.secondary">
              Net Recharge
            </Typography>

            <Typography variant="h4" color="success.main">
              {summary.recharge_days ?? 0}
            </Typography>
          </Paper>
        </Grid>

        <Grid item xs={12} md={3}>
          <Paper sx={{ p: 2 }}>
            <Typography color="text.secondary">
              Net Depletion
            </Typography>

            <Typography variant="h4" color="error.main">
              {summary.depletion_days ?? 0}
            </Typography>
          </Paper>
        </Grid>

        <Grid item xs={12} md={3}>
          <Paper sx={{ p: 2 }}>
            <Typography color="text.secondary">
              Latest ΔS
            </Typography>

            <Typography
              variant="h4"
              color={
               summary.average_delta_s?.toFixed(2) ?? "--" >= 0
                  ? "success.main"
                  : "error.main"
              }
            >
              {history[0]?.delta_s ?? "--"}
            </Typography>
          </Paper>
        </Grid>

      </Grid>

      {/* SEARCH */}

      <TextField
        fullWidth
        label="Search by Date / Timestamp"
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        sx={{ mb: 3 }}
      />

      {/* TABLE */}

      <Card>

        <TableContainer>

          <Table>

            <TableHead>

              <TableRow>

                <TableCell>ID</TableCell>

                <TableCell>Date</TableCell>

                <TableCell>Time</TableCell>

                <TableCell>Timestamp</TableCell>

                <TableCell align="center">ΔS</TableCell>

                <TableCell>Status</TableCell>

              </TableRow>

            </TableHead>

            <TableBody>

              {filteredHistory.map((item, index) => (

                <TableRow
                  key={item.id}
                  sx={{
                    backgroundColor:
                      index === 0 ? "#E3F2FD" : "inherit",
                  }}
                >

                  <TableCell>{item.id}</TableCell>

                  <TableCell>
                    {item.date}
                  </TableCell>

                  <TableCell>
                    {item.date}
                  </TableCell>

                  <TableCell>
                    {`${item.date} ${item.time}`}
                  </TableCell>

                  <TableCell
                    align="center"
                    sx={{
                      fontWeight: "bold",
                      color:
                        item.delta_s >= 0
                          ? "green"
                          : "red",
                    }}
                  >
                    {item.delta_s >= 0 ? "⬆ " : "⬇ "}
                    {item.delta_s}
                  </TableCell>

                  <TableCell>

                    <Chip
                      color={
                        item.delta_s >= 0
                          ? "success"
                          : "error"
                      }
                      label={
                        item.delta_s >= 0
                          ? "Net Recharge"
                          : "Net Depletion"
                      }
                    />

                    {index === 0 && (
                      <Chip
                        label="Latest"
                        color="primary"
                        size="small"
                        sx={{ ml: 1 }}
                      />
                    )}

                  </TableCell>

                </TableRow>

              ))}

            </TableBody>

          </Table>

        </TableContainer>

      </Card>

        </Box>

  </Box>
);
}