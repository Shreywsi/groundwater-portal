import { useState } from "react";
import { useNavigate } from "react-router-dom";
import PublicLayout from "../layouts/PublicLayout";
import { useTranslation } from "react-i18next";
import {
  Container,
  Paper,
  Typography,
  TextField,
  Button,
  MenuItem,
  Box
} from "@mui/material";

function LoginPage() {
    const { t } = useTranslation();

  const navigate = useNavigate();

  const [role, setRole] = useState("");

  const handleLogin = () => {

    if (role === "admin") {
      navigate("/admin");
    }

    if (role === "farmer") {
      navigate("/farmer");
    }

    if (role === "crp") {
      navigate("/crp");
    }

    if (role === "researcher") {
      navigate("/researcher");
    }

  };

  return (
    <PublicLayout>
        <Container maxWidth="sm">
      <Box
        sx={{
          minHeight: "100vh",
          display: "flex",
          alignItems: "center"
        }}
      >
        <Paper
          elevation={5}
          sx={{
            p: 4,
            width: "100%",
            borderRadius: 3
          }}
        >
          <Typography variant="h4" align="center" gutterBottom>
           {t("title")}
          </Typography>

          <Typography
            align="center"
            color="text.secondary"
            mb={3}
          >
            {t("subtitle")}
          </Typography>

          <TextField
            fullWidth
            label={t("username")}
            margin="normal"
          />

          <TextField
            fullWidth
            label={t("password")}
            type="password"
            margin="normal"
          />

          <TextField
            fullWidth
            select
            label={t("role")}
            margin="normal"
            value={role}
            onChange={(e) => setRole(e.target.value)}
          >
            <MenuItem value="admin">Admin</MenuItem>
            <MenuItem value="farmer">Farmer</MenuItem>
            <MenuItem value="crp">CRP</MenuItem>
            <MenuItem value="researcher">Researcher</MenuItem>
          </TextField>

          <Button
            variant="contained"
            fullWidth
            size="large"
            sx={{ mt: 3 }}
            onClick={handleLogin}
          >
            Login
          </Button>

        </Paper>
      </Box>
    </Container>
    </PublicLayout>
    );
}

export default LoginPage;