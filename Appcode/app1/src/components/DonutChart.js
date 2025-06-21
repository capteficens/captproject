import React from "react";
import { PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer } from "recharts";

export const DonutChart = () => {
  const data = [
    { name: "LinkedIn", value: 40 },
    { name: "Indeed", value: 30 },
    { name: "Glassdoor", value: 20 },
    { name: "Dice", value: 10 },
  ];

  const COLORS = ["#1E3A8A", "#3B82F6", "#93C5FD", "#BFDBFE"];

  return (
    <div className="bg-white p-4 rounded-lg shadow">
      <h2 className="text-lg font-semibold text-blue-900 mb-2">Platform Breakdown</h2>
      <ResponsiveContainer width="100%" height={250}>
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            innerRadius={50}
            outerRadius={80}
            fill="#8884d8"
            dataKey="value"
            label
          >
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip />
          <Legend />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
};
