import React from "react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";

export const LineChartSection = () => {
  const data = [
    { month: "Jan", value: 2 },
    { month: "Feb", value: 5 },
    { month: "Mar", value: 3 },
    { month: "Apr", value: 8 },
    { month: "May", value: 11 },
    { month: "Jun", value: 10 },
    { month: "Jul", value: 6 },
  ];

  return (
    <div className="bg-white p-4 rounded-lg shadow mb-6">
      <h2 className="text-lg font-semibold text-blue-900 mb-2">Applications Over Time</h2>
      <ResponsiveContainer width="100%" height={250}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="month" />
          <YAxis />
          <Tooltip />
          <Line type="monotone" dataKey="value" stroke="#1D4ED8" strokeWidth={2} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};
