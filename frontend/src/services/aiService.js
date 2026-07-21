import API_BASE from "../config/api";

const API = API_BASE;

export async function getAIDashboard() {
    const response = await fetch(`${API}/ml/dashboard/`);

    if (!response.ok) {
        throw new Error("Failed to load AI dashboard.");
    }

    return await response.json();
}