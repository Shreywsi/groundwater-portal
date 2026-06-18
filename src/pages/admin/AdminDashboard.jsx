import MainLayout from "../../layouts/MainLayout";
import DashboardCard from "../../components/DashboardCard";

import {
  Typography,
  Grid
} from "@mui/material";

function AdminDashboard() {
  return (
    <MainLayout>

      <Typography
        variant="h4"
        gutterBottom
      >
        Admin Dashboard
      </Typography>

      <Grid container spacing={3}>

        <Grid item xs={12} md={3}>
          <DashboardCard
            title="Total Users"
            value="50"
          />
        </Grid>

        <Grid item xs={12} md={3}>
          <DashboardCard
            title="Villages"
            value="15"
          />
        </Grid>

        <Grid item xs={12} md={3}>
          <DashboardCard
            title="Farmers"
            value="300"
          />
        </Grid>

        <Grid item xs={12} md={3}>
          <DashboardCard
            title="Wells"
            value="750"
          />
        </Grid>

      </Grid>

    </MainLayout>
  );
}

export default AdminDashboard;