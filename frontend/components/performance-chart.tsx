'use client';

import { Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';

const data = [
  { name: 'W1', roi: 4 },
  { name: 'W2', roi: 6 },
  { name: 'W3', roi: 2 },
  { name: 'W4', roi: 8 },
];

export function PerformanceChart() {
  return (
    <div className="h-64 rounded-xl border border-slate-800 bg-slate-900 p-4">
      <p className="mb-2 text-sm text-slate-300">Agent ROI Trend</p>
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data}>
          <XAxis dataKey="name" stroke="#94a3b8" />
          <YAxis stroke="#94a3b8" />
          <Tooltip />
          <Line type="monotone" dataKey="roi" stroke="#22d3ee" strokeWidth={2} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
