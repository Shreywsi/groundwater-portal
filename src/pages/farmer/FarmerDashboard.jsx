import FarmerLayout from "../../layouts/FarmerLayout";

import {
  Typography,
  Grid,
  Card,
  CardActionArea,
  CardContent,
  Container,
  Alert
} from "@mui/material";

import {
  Cloud,
  Agriculture,
  History,
  SupportAgent,
  Mic,
  CloudOff
} from "@mui/icons-material";

import { useNavigate } from "react-router-dom";

function FarmerDashboard() {
  const navigate = useNavigate();

  return (
    <FarmerLayout>
      <Container maxWidth="lg">

        {/* Connectivity Status */}

        <Alert
          severity="success"
          sx={{
            mb: 4,
            borderRadius: 3
          }}
        >
          Connected to Internet
        </Alert>

        {/* Welcome */}

        <Typography
          sx={{
            fontWeight: "bold",
            fontSize: {
              xs: "1.8rem",
              sm: "2.2rem"
            }
          }}
        >
          Welcome, Ramesh 👋
        </Typography>

        <Typography
          color="text.secondary"
          sx={{ mb: 5 }}
        >
          Village: Rampura
        </Typography>

        <Grid container spacing={4}>

          {/* Rainfall */}

          <Grid item xs={12} sm={6} md={4}>
            <Card sx={{ borderRadius: 5, minHeight: 220 }}>
              <CardActionArea
                sx={{ height: "100%" }}
                onClick={() => navigate("/farmer/rainfall")}
              >
                <CardContent
                  sx={{
                    display: "flex",
                    flexDirection: "column",
                    justifyContent: "center",
                    alignItems: "center",
                    gap: 2
                  }}
                >
                  <Cloud
                    sx={{
                      fontSize: {
                        xs: 55,
                        sm: 70
                      },
                      color: "#2196f3"
                    }}
                  />

                  <Typography variant="h5" fontWeight="bold">
                    Rainfall
                  </Typography>

                  <Typography
                    align="center"
                    color="text.secondary"
                  >
                    Record today's rainfall
                  </Typography>

                </CardContent>
              </CardActionArea>
            </Card>
          </Grid>

          {/* Pumping */}

          <Grid item xs={12} sm={6} md={4}>
            <Card sx={{ borderRadius: 5, minHeight: 220 }}>
              <CardActionArea
                sx={{ height: "100%" }}
                onClick={() => navigate("/farmer/pumping")}
              >
                <CardContent
                  sx={{
                    display: "flex",
                    flexDirection: "column",
                    justifyContent: "center",
                    alignItems: "center",
                    gap: 2
                  }}
                >
                  <Agriculture
                    sx={{
                      fontSize: {
                        xs: 55,
                        sm: 70
                      },
                      color: "#ff9800"
                    }}
                  />

                  <Typography variant="h5" fontWeight="bold">
                    Pumping
                  </Typography>

                  <Typography
                    align="center"
                    color="text.secondary"
                  >
                    Record irrigation hours
                  </Typography>

                </CardContent>
              </CardActionArea>
            </Card>
          </Grid>

          {/* History */}

          <Grid item xs={12} sm={6} md={4}>
            <Card sx={{ borderRadius: 5, minHeight: 220 }}>
              <CardActionArea
                sx={{ height: "100%" }}
                onClick={() => navigate("/farmer/history")}
              >
                <CardContent
                  sx={{
                    display: "flex",
                    flexDirection: "column",
                    justifyContent: "center",
                    alignItems: "center",
                    gap: 2
                  }}
                >
                  <History
                    sx={{
                      fontSize: {
                        xs: 55,
                        sm: 70
                      },
                      color: "#4caf50"
                    }}
                  />

                  <Typography variant="h5" fontWeight="bold">
                    History
                  </Typography>

                  <Typography
                    align="center"
                    color="text.secondary"
                  >
                    View previous entries
                  </Typography>

                </CardContent>
              </CardActionArea>
            </Card>
          </Grid>

          {/* Voice Entry */}

          <Grid item xs={12} sm={6} md={4}>
            <Card sx={{ borderRadius: 5, minHeight: 220 }}>
              <CardActionArea>
                <CardContent
                  sx={{
                    display: "flex",
                    flexDirection: "column",
                    justifyContent: "center",
                    alignItems: "center",
                    gap: 2
                  }}
                >
                  <Mic
                    sx={{
                      fontSize: {
                        xs: 55,
                        sm: 70
                      },
                      color: "#e91e63"
                    }}
                  />

                  <Typography variant="h5" fontWeight="bold">
                    Voice Entry
                  </Typography>

                  <Typography
                    align="center"
                    color="text.secondary"
                  >
                    Speak rainfall or pumping hours
                  </Typography>

                </CardContent>
              </CardActionArea>
            </Card>
          </Grid>

          {/* Offline Mode */}

          <Grid item xs={12} sm={6} md={4}>
            <Card sx={{ borderRadius: 5, minHeight: 220 }}>
              <CardContent
                sx={{
                  display: "flex",
                  flexDirection: "column",
                  justifyContent: "center",
                  alignItems: "center",
                  gap: 2
                }}
              >
                <CloudOff
                  sx={{
                    fontSize: {
                      xs: 55,
                      sm: 70
                    },
                    color: "#795548"
                  }}
                />

                <Typography variant="h5" fontWeight="bold">
                  Offline Mode
                </Typography>

                <Typography
                  align="center"
                  color="text.secondary"
                >
                  Data will sync when internet returns
                </Typography>

              </CardContent>
            </Card>
          </Grid>

          {/* Contact CRP */}

          <Grid item xs={12} sm={6} md={4}>
            <Card sx={{ borderRadius: 5, minHeight: 220 }}>
              <CardActionArea>
                <CardContent
                  sx={{
                    display: "flex",
                    flexDirection: "column",
                    justifyContent: "center",
                    alignItems: "center",
                    gap: 2
                  }}
                >
                  <SupportAgent
                    sx={{
                      fontSize: {
                        xs: 55,
                        sm: 70
                      },
                      color: "#9c27b0"
                    }}
                  />

                  <Typography variant="h5" fontWeight="bold">
                    Contact CRP
                  </Typography>

                  <Typography
                    align="center"
                    color="text.secondary"
                  >
                    Need help? Contact your Community Resource Person
                  </Typography>

                </CardContent>
              </CardActionArea>
            </Card>
          </Grid>

        </Grid>

      </Container>
    </FarmerLayout>
  );
}

export default FarmerDashboard;