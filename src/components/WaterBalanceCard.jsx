import { useMemo, useState } from "react";
import {
  Box,
  Card,
  Typography,
  Button,
  Collapse,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TextField,
  Stack,
  Divider,
  Chip
} from "@mui/material";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import ExpandLessIcon from "@mui/icons-material/ExpandLess";

/*
 * Water Balance Equation:
 *   Rr + Re + Ri + I + Si  =  Se + O + Et + Dp + ΔS
 *   (Inflow terms)             (Outflow terms)   (Change in storage)
 *
 * => ΔS = (Rr + Re + Ri + I + Si) - (Se + O + Et + Dp)
 *
 * ΔS > 0  → storage is increasing (net recharge)
 * ΔS < 0  → storage is decreasing (net depletion)
 */

// Definitions for each term — used for labels + tooltips in the table
const INFLOW_FIELDS = [
  { key: "Rr", label: "Rr — Recharge due to rainfall" },
  { key: "Re", label: "Re — Recharge due to canal seepage" },
  { key: "Ri", label: "Ri — Recharge due to return flow of applied irrigation water" },
  { key: "I", label: "I — Inflow from areas outside the basin" },
  { key: "Si", label: "Si — Recharge due to inflow seepage (rivers/streams/reservoirs/lakes/ponds)" }
];

const OUTFLOW_FIELDS = [
  { key: "Se", label: "Se — Groundwater flow due to effluent seepage" },
  { key: "O", label: "O — Outflow to areas outside the basin" },
  { key: "Et", label: "Et — Evapo-transpiration losses" },
  { key: "Dp", label: "Dp — Groundwater draft (pumpage)" }
];

const DEFAULT_VALUES = {
  Rr: 0,
  Re: 0,
  Ri: 0,
  I: 0,
  Si: 0,
  Se: 0,
  O: 0,
  Et: 0,
  Dp: 0
};

// Small helper: format numbers with 2 decimals, no trailing junk
const fmt = (n) => {
  if (Number.isNaN(n)) return "0.00";
  return n.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 });
};

export default function WaterBalanceCard({
  initialValues = DEFAULT_VALUES,
  unit = "MCM", // e.g. Million Cubic Meters — change to match your data's unit
  onChange // optional callback(values, deltaS) if the parent wants to persist data
}) {
  const [values, setValues] = useState({ ...DEFAULT_VALUES, ...initialValues });
  const [expanded, setExpanded] = useState(false);

  const totals = useMemo(() => {
    const inflow = INFLOW_FIELDS.reduce((sum, f) => sum + (Number(values[f.key]) || 0), 0);
    const outflow = OUTFLOW_FIELDS.reduce((sum, f) => sum + (Number(values[f.key]) || 0), 0);
    const deltaS = inflow - outflow;
    return { inflow, outflow, deltaS };
  }, [values]);

  const handleFieldChange = (key, raw) => {
    // Allow empty string while typing, otherwise parse as float
    const next = { ...values, [key]: raw === "" ? "" : Number(raw) };
    setValues(next);
    if (onChange) onChange(next, computeDeltaS(next));
  };

  const computeDeltaS = (v) => {
    const inflow = INFLOW_FIELDS.reduce((sum, f) => sum + (Number(v[f.key]) || 0), 0);
    const outflow = OUTFLOW_FIELDS.reduce((sum, f) => sum + (Number(v[f.key]) || 0), 0);
    return inflow - outflow;
  };

  const isSurplus = totals.deltaS >= 0;

  return (
    <Card
      elevation={3}
      sx={{
        p: { xs: 2, sm: 3, md: 4 },
        borderRadius: 3
      }}
    >
      {/* Header row: title + the headline balance value */}
      <Stack
        direction={{ xs: "column", sm: "row" }}
        justifyContent="space-between"
        alignItems={{ xs: "flex-start", sm: "center" }}
        spacing={2}
      >
        <Box>
          <Typography variant="h6">Water Balance</Typography>
          <Typography variant="body2" color="text.secondary">
            ΔS = (Rr + Re + Ri + I + Si) − (Se + O + Et + Dp)
          </Typography>
        </Box>

        <Stack direction="row" spacing={1} alignItems="center">
          <Typography
            variant="h4"
            fontWeight="bold"
            color={isSurplus ? "success.main" : "error.main"}
          >
            {fmt(totals.deltaS)} {unit}
          </Typography>
          <Chip
            size="small"
            color={isSurplus ? "success" : "error"}
            label={isSurplus ? "Net Recharge" : "Net Depletion"}
          />
        </Stack>
      </Stack>

      <Box sx={{ mt: 2 }}>
        <Button
          size="small"
          onClick={() => setExpanded((e) => !e)}
          endIcon={expanded ? <ExpandLessIcon /> : <ExpandMoreIcon />}
        >
          {expanded ? "Hide details" : "See more"}
        </Button>
      </Box>

      <Collapse in={expanded} timeout="auto" unmountOnExit>
        <Divider sx={{ my: 2 }} />

        <Stack spacing={4}>
          {/* INFLOW TABLE */}
          <Box>
            <Typography variant="subtitle1" fontWeight="bold" gutterBottom>
              Inflow components
            </Typography>
            <TableContainer>
              <Table size="small">
                <TableHead>
                  <TableRow>
                    <TableCell>Component</TableCell>
                    <TableCell align="right" width={160}>
                      Value ({unit})
                    </TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {INFLOW_FIELDS.map((f) => (
                    <TableRow key={f.key}>
                      <TableCell>{f.label}</TableCell>
                      <TableCell align="right">
                        <TextField
                          size="small"
                          type="number"
                          value={values[f.key]}
                          onChange={(e) => handleFieldChange(f.key, e.target.value)}
                          inputProps={{ style: { textAlign: "right" }, step: "any" }}
                          sx={{ width: 120 }}
                        />
                      </TableCell>
                    </TableRow>
                  ))}
                  <TableRow>
                    <TableCell>
                      <strong>Total Inflow</strong>
                    </TableCell>
                    <TableCell align="right">
                      <strong>{fmt(totals.inflow)}</strong>
                    </TableCell>
                  </TableRow>
                </TableBody>
              </Table>
            </TableContainer>
          </Box>

          {/* OUTFLOW TABLE */}
          <Box>
            <Typography variant="subtitle1" fontWeight="bold" gutterBottom>
              Outflow components
            </Typography>
            <TableContainer>
              <Table size="small">
                <TableHead>
                  <TableRow>
                    <TableCell>Component</TableCell>
                    <TableCell align="right" width={160}>
                      Value ({unit})
                    </TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {OUTFLOW_FIELDS.map((f) => (
                    <TableRow key={f.key}>
                      <TableCell>{f.label}</TableCell>
                      <TableCell align="right">
                        <TextField
                          size="small"
                          type="number"
                          value={values[f.key]}
                          onChange={(e) => handleFieldChange(f.key, e.target.value)}
                          inputProps={{ style: { textAlign: "right" }, step: "any" }}
                          sx={{ width: 120 }}
                        />
                      </TableCell>
                    </TableRow>
                  ))}
                  <TableRow>
                    <TableCell>
                      <strong>Total Outflow</strong>
                    </TableCell>
                    <TableCell align="right">
                      <strong>{fmt(totals.outflow)}</strong>
                    </TableCell>
                  </TableRow>
                </TableBody>
              </Table>
            </TableContainer>
          </Box>

          {/* Summary line */}
          <Box
            sx={{
              p: 2,
              borderRadius: 2,
              bgcolor: isSurplus ? "rgba(46, 125, 50, 0.08)" : "rgba(211, 47, 47, 0.08)",
              border: "1px solid",
              borderColor: isSurplus ? "success.light" : "error.light"
            }}
          >
            <Typography variant="body2">
              Total Inflow ({fmt(totals.inflow)}) − Total Outflow ({fmt(totals.outflow)}) ={" "}
              <strong>ΔS = {fmt(totals.deltaS)} {unit}</strong>{" "}
              ({isSurplus ? "groundwater storage is increasing" : "groundwater storage is decreasing"})
            </Typography>
          </Box>
        </Stack>
      </Collapse>
    </Card>
  );
}