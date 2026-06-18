import FarmerLayout from "../../layouts/FarmerLayout";
import {
  Container,
  Typography,
  Stack,
  Grid,
  Card,
  CardActionArea,
  CardContent,
  Box,
  Alert
} from "@mui/material";

import {
  Cloud,
  Agriculture,
  History,
  Mic,
  CloudOff,
  SupportAgent
} from "@mui/icons-material";

import { useNavigate } from "react-router-dom";
import { useTranslation } from "react-i18next";

function FarmerDashboard() {
  const navigate = useNavigate();
  const { t } = useTranslation();

  const cards = [
  {
    title: t("rainfall"),
    subtitle: t("rainfall_subtitle"),
    icon: Cloud,
    color: "#2196f3",
    path: "/farmer/rainfall"
  },
  {
    title: t("pumping"),
    subtitle: t("pumping_subtitle"),
    icon: Agriculture,
    color: "#ff9800",
    path: "/farmer/pumping"
  },
  {
    title: t("history"),
    subtitle: t("history_subtitle"),
    icon: History,
    color: "#4caf50",
    path: "/farmer/history"
  },
  {
    title: t("voice_entry"),
    subtitle: t("voice_entry_subtitle"),
    icon: Mic,
    color: "#e91e63"
  },
  {
    title: t("offline_mode"),
    subtitle: t("offline_mode_subtitle"),
    icon: CloudOff,
    color: "#795548"
  },
  {
    title: t("contact_crp"),
    subtitle: t("contact_crp_subtitle"),
    icon: SupportAgent,
    color: "#9c27b0"
  }
];

  return (
    <FarmerLayout>
      <Container
        maxWidth="xl"
        sx={{
          py: { xs: 2, md: 4 }
        }}
      >
        <Stack spacing={4}>

          {/* Internet status */}

          <Alert severity="success">
            {t("connected")}
          </Alert>

          {/* Header */}

          <Box>
            <Typography
              variant="h4"
              fontWeight="bold"
              sx={{
                fontSize: {
                  xs: "1.8rem",
                  sm: "2rem",
                  md: "2.3rem"
                }
              }}
            >
              {t("welcome")} 👋
            </Typography>

            <Typography
              color="text.secondary"
              sx={{
                mt: 1,
                fontSize: {
                  xs: "0.95rem",
                  md: "1rem"
                }
              }}
            >
              {t("village_name")}
            </Typography>
          </Box>

          {/* Cards */}

          <Grid container spacing={3}>
            {cards.map((card) => {
              const Icon = card.icon;

              return (
                <Grid
                  item
                  xs={12}
                  sm={6}
                  md={4}
                  key={card.title}
                >
                  <Card
                    sx={{
                      borderRadius: 4,
                      height: "100%",
                      transition: "0.3s",
                      "&:hover": {
                        transform: "translateY(-5px)",
                        boxShadow: 6
                      }
                    }}
                  >
                    <CardActionArea
                      sx={{
                        height: "100%",
                        p: 3
                      }}
                      onClick={() => {
                        if (card.path) {
                          navigate(card.path);
                        }
                      }}
                    >
                      <CardContent>

                        <Box
                          sx={{
                            width: 70,
                            height: 70,
                            borderRadius: 3,
                            backgroundColor: `${card.color}20`,
                            display: "flex",
                            alignItems: "center",
                            justifyContent: "center",
                            mb: 3
                          }}
                        >
                          <Icon
                            sx={{
                              fontSize: 40,
                              color: card.color
                            }}
                          />
                        </Box>

                        <Typography
                          variant="h6"
                          fontWeight="bold"
                        >
                          {card.title}
                        </Typography>

                        <Typography
                          color="text.secondary"
                          sx={{ mt: 1 }}
                        >
                          {card.subtitle}
                        </Typography>

                      </CardContent>
                    </CardActionArea>
                  </Card>
                </Grid>
              );
            })}
          </Grid>

        </Stack>
      </Container>
    </FarmerLayout>
  );
}

export default FarmerDashboard;