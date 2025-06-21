import React from "react";

export const FunnelChart = () => {
  const stages = ["Application", "Calls", "Interviews", "Offers"];
  const widths = ["w-full", "w-3/4", "w-1/2", "w-1/3"];

  return (
    <div className="bg-white p-4 rounded-lg shadow">
      <h2 className="text-lg font-semibold text-blue-900 mb-2">Funnel</h2>
      <div className="flex flex-col gap-2">
        {stages.map((stage, i) => (
          <div key={stage} className={`bg-blue-600 h-6 ${widths[i]} rounded-md mx-auto`} />
        ))}
      </div>
    </div>
  );
};
