import axios from "axios";

import API_BASE from "../config/api";

const API = API_BASE;

export const retrainModel = async () => {
  const res = await axios.post(`${API}/ml/retrain/`);
  return res.data;
};