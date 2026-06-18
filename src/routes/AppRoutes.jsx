import { BrowserRouter, Routes, Route } from "react-router-dom";

import LoginPage from "../pages/LoginPage";
import AdminDashboard from "../pages/admin/AdminDashboard";

import FarmerDashboard from "../pages/farmer/FarmerDashboard";
import Rainfall from "../pages/farmer/Rainfall";
import Pumping from "../pages/farmer/Pumping";
import MyWells from "../pages/farmer/MyWells";
import History from "../pages/farmer/History";

import CRPDashboard from "../pages/crp/CRPDashboard";
import ResearcherDashboard from "../pages/researcher/ResearcherDashboard";

function AppRoutes() {
  return (
    <BrowserRouter>
      <Routes>

        <Route path="/" element={<LoginPage />} />

        <Route path="/admin" element={<AdminDashboard />} />

        <Route path="/farmer" element={<FarmerDashboard />} />
        <Route path="/farmer/rainfall" element={<Rainfall />} />

        <Route path="/farmer/pumping" element={<Pumping />} />

        <Route path="/farmer/wells" element={<MyWells />} />

        <Route path="/farmer/history" element={<History />} />

        <Route path="/crp" element={<CRPDashboard />} />

        <Route path="/researcher" element={<ResearcherDashboard />} />

      </Routes>
    </BrowserRouter>
  );
}

export default AppRoutes;