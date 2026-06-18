import FarmerLayout from "../../layouts/FarmerLayout";
import {
  Typography,
  Card,
  CardContent
} from "@mui/material";

function MyWells() {
  return (
    <FarmerLayout>

      <Typography variant="h4" gutterBottom>
        💧 My Wells
      </Typography>

      <Card sx={{ mb: 3 }}>
        <CardContent>

          <Typography variant="h6">
            Well ID : W001
          </Typography>

          <Typography>
            Village : Rampura
          </Typography>

          <Typography>
            Depth : 120 m
          </Typography>

          <Typography>
            Current Water Level : 18.5 m
          </Typography>

        </CardContent>
      </Card>

    </FarmerLayout>
  );
}

export default MyWells;