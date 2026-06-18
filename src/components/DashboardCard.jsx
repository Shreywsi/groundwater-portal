import {
  Card,
  CardContent,
  Typography
} from "@mui/material";

function DashboardCard({ title, value }) {
  return (
    <Card elevation={4}>

      <CardContent>

        <Typography variant="h6">
          {title}
        </Typography>

        <Typography
          variant="h4"
          color="primary"
        >
          {value}
        </Typography>

      </CardContent>

    </Card>
  );
}

export default DashboardCard;