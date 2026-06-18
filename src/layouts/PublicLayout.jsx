import { Box, Toolbar } from "@mui/material";
import PublicNavbar from "../components/PublicNavbar";

function PublicLayout({ children }) {

  return (
    <Box
      sx={{
        minHeight: "100vh",
        backgroundColor: "#f5f7fa"
      }}
    >

      <PublicNavbar />

      <Toolbar />

      <Box>
        {children}
      </Box>

    </Box>
  );
}

export default PublicLayout;