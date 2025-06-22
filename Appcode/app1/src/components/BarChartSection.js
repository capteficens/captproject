import React from "react";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

export const BarChartSection = () => {
  const data = [
    { title: "Software Engineer", value: 12 },
    { title: "Data Analyst", value: 8 },
    { title: "Project Manager", value: 6 },
    { title: "Marketing Specialist", value: 5 },
    { title: "Financial Analyst", value: 4 },
  ];

  return (
    <div className="bg-white p-4 rounded-lg shadow mt-6">
      <h2 className="text-lg font-semibold text-blue-900 mb-2">Top Job Titles</h2>
      <ResponsiveContainer width="100%" height={250}>
        <BarChart data={data} layout="vertical">
          <XAxis type="number" />
          <YAxis dataKey="title" type="category" />
          <Tooltip />
          <Bar dataKey="value" fill="#2563EB" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};
