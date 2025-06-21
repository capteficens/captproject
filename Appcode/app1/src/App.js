import React from "react";
import { Metrics } from "./components/Metrics";
import { LineChartSection } from "./components/LineChartSection";
import { DonutChart } from "./components/DonutChart";
import { FunnelChart } from "./components/FunnelChart";
import { BarChartSection } from "./components/BarChartSection";

function App() {
  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <div className="bg-white rounded-xl shadow p-6 max-w-6xl mx-auto">
        <h1 className="text-2xl font-bold text-blue-900 mb-6">
          Candidate Performance Dashboard
        </h1>
        <Metrics />
        <LineChartSection />
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <FunnelChart />
          <DonutChart />
        </div>
        <BarChartSection />
      </div>
    </div>
  );
}

export default App;
