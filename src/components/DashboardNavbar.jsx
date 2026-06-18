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
      <Toolbar
        sx={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          gap: 1
        }}
      >
        {/* Title */}
        <Typography
          variant="h6"
          sx={{
            flexGrow: 1,
            fontWeight: "bold",
            fontSize: {
              xs: "1rem",
              sm: "1.2rem",
              md: "1.4rem"
            }
          }}
        >
          {/* Desktop */}
          <Box
            component="span"
            sx={{
              display: {
                xs: "none",
                sm: "inline"
              }
            }}
          >
            Groundwater Management Portal
          </Box>

          {/* Mobile */}
          <Box
            component="span"
            sx={{
              display: {
                xs: "inline",
                sm: "none"
              }
            }}
          >
            GW Portal
          </Box>
        </Typography>

        {/* Right section */}
        <Box
          sx={{
            display: "flex",
            alignItems: "center",
            gap: {
              xs: 0.5,
              sm: 1.5
            }
          }}
        >
          <LanguageSelector />

          <IconButton color="inherit" size="small">
            <NotificationsIcon />
          </IconButton>

          <IconButton color="inherit" size="small">
            <AccountCircleIcon />
          </IconButton>
        </Box>
      </Toolbar>
    </AppBar>
  );
}

export default DashboardNavbar;