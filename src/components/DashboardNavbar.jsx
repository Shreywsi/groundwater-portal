import {
  AppBar,
  Toolbar,
  Typography,
  Box,
  IconButton
} from "@mui/material";

import NotificationsIcon from "@mui/icons-material/Notifications";
import AccountCircleIcon from "@mui/icons-material/AccountCircle";

import LanguageSelector from "./LanguageSelector";

function DashboardNavbar() {

  return (
    <AppBar position="fixed">

      <Toolbar>

        <Typography
          variant="h6"
          sx={{ flexGrow: 1 }}
        >
          Groundwater Management Portal
        </Typography>

        <Box
          sx={{
            display: "flex",
            alignItems: "center",
            gap: 2
          }}
        >
          <LanguageSelector />

          <IconButton color="inherit">
            <NotificationsIcon />
          </IconButton>

          <IconButton color="inherit">
            <AccountCircleIcon />
          </IconButton>

        </Box>

      </Toolbar>

    </AppBar>
  );
}

export default DashboardNavbar;