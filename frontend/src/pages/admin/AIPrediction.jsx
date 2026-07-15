import { Container, Typography } from "@mui/material";
import AIPredictionCard from "../../components/admin/AIPredictionCard";

export default function AIPrediction() {
  return (
    <Container maxWidth="xl" sx={{ mt: 4 }}>
      <Typography variant="h4" fontWeight="bold" gutterBottom>
        🤖 AI Prediction Module
      </Typography>

      <Typography color="text.secondary" sx={{ mb: 3 }}>
        Groundwater forecasting using AI models.
      </Typography>

      <AIPredictionCard />
    </Container>
  );
}