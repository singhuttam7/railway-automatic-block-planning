import { BrowserRouter, Routes, Route } from "react-router-dom";
import Layout from "./components/Layout";
import Dashboard from "./pages/Dashboard";
import Maintenance from "./pages/Maintenance";
import Corridors from "./pages/Corridors";
import BlockPlanning from "./pages/BlockPlanning";
import TrainsForecast from "./pages/TrainsForecast";
import WhatIfSimulator from "./pages/WhatIfSimulator";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route path="/" element={<Dashboard />} />
          <Route path="/maintenance" element={<Maintenance />} />
          <Route path="/corridors" element={<Corridors />} />
          <Route path="/blocks" element={<BlockPlanning />} />
          <Route path="/trains" element={<TrainsForecast />} />
          <Route path="/ai-intelligence" element={<WhatIfSimulator />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
