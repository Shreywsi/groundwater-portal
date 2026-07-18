import { useEffect, useState } from "react";
import { Box, CircularProgress } from "@mui/material";
import API_BASE from "../../config/api";
import PredictionInsights from "../ai/PredictionInsights";

export default function AIPredictionCard() {
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchPrediction = async () => {
      try {
        const response = await fetch(`${API_BASE}/predict/`);
        const data = await response.json();
        setPrediction(data);
      } catch (error) {
        console.error("Prediction API error:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchPrediction();
  }, []);

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" py={6}>
        <CircularProgress />
      </Box>
    );
  }

  return <PredictionInsights prediction={prediction} />;
}