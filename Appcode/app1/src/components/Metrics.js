import React from "react";

export const Metrics = () => {
  const data = [
    { label: "Applications", value: 45 },
    { label: "Calls", value: 15 },
    { label: "Interviews", value: 8 },
    { label: "Submissions", value: 3 },
  ];

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
      {data.map((item) => (
        <div key={item.label} className="bg-blue-50 p-4 rounded-lg text-center shadow">
          <p className="text-3xl font-bold text-blue-900">{item.value}</p>
          <p className="text-sm uppercase text-blue-700">{item.label}</p>
        </div>
      ))}
    </div>
  );
};
