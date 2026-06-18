import FarmerLayout from "../../layouts/FarmerLayout";
import {
  Typography,
  Card,
  CardContent
} from "@mui/material";

function History() {
  return (
    <FarmerLayout>

      <Typography variant="h4" gutterBottom>
        📜 History
      </Typography>

      <Card>
        <CardContent>

          <Typography>
            10 June - Rainfall: 15 mm
          </Typography>

          <Typography>
            12 June - Pumping: 4 Hours
          </Typography>

          <Typography>
            15 June - Rainfall: 10 mm
          </Typography>

        </CardContent>
      </Card>

    </FarmerLayout>
  );
}

export default History;