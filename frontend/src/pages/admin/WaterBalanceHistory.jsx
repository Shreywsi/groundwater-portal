import { useEffect, useState } from "react";
import axios from "axios";

import {
  Card,
  Typography,
  Table,
  TableHead,
  TableRow,
  TableCell,
  TableBody,
  TableContainer,
  Chip,
  Box,
} from "@mui/material";

export default function WaterBalanceHistory() {
  const [history, setHistory] = useState([]);

  useEffect(() => {
    loadHistory();
  }, []);

  const loadHistory = async () => {
    try {
      const res = await axios.get(
        "http://127.0.0.1:8000/api/water-balance/history/"
      );

      setHistory(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <Card sx={{ p: 3 }}>
      <Typography variant="h5" gutterBottom>
        Water Balance History
      </Typography>

      <TableContainer>
        <Table>

          <TableHead>

            <TableRow>
              <TableCell>ID</TableCell>
              <TableCell>Date</TableCell>
              <TableCell>Time</TableCell>
              <TableCell>ΔS</TableCell>
              <TableCell>Status</TableCell>
            </TableRow>

          </TableHead>

          <TableBody>

            {history.map((item) => (

              <TableRow key={item.id}>

                <TableCell>{item.id}</TableCell>

                <TableCell>
                  {new Date(item.created_at).toLocaleDateString()}
                </TableCell>

                <TableCell>
                  {new Date(item.created_at).toLocaleTimeString()}
                </TableCell>

                <TableCell>{item.delta_s}</TableCell>

                <TableCell>

                  <Chip
                    color={item.delta_s >= 0 ? "success" : "error"}
                    label={
                      item.delta_s >= 0
                        ? "Net Recharge"
                        : "Net Depletion"
                    }
                  />

                </TableCell>

              </TableRow>

            ))}

          </TableBody>

        </Table>
      </TableContainer>
    </Card>
  );
}