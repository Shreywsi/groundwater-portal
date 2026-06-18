import {
  AppBar,
  Toolbar,
  Typography,
  Box
} from "@mui/material";

import LanguageSelector from "./LanguageSelector";

function Navbar() {

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
            alignItems: "center"
          }}
        >
          <LanguageSelector />
        </Box>

      </Toolbar>

    </AppBar>
  );
}

export default Navbar;