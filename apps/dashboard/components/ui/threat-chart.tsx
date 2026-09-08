"use client";

import {
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

const data = [
  { time: "00:00", alerts: 12 },
  { time: "04:00", alerts: 19 },
  { time: "08:00", alerts: 3 },
  { time: "12:00", alerts: 45 },
  { time: "16:00", alerts: 22 },
  { time: "20:00", alerts: 14 },
  { time: "24:00", alerts: 8 },
];

export function ThreatChart() {
  return (
    <div className="h-[300px] w-full p-4 border rounded-xl bg-card">
      <h3 className="font-medium text-sm text-muted-foreground mb-4">
        Threat Volume over Time
      </h3>
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data}>
          <XAxis
            dataKey="time"
            stroke="#888888"
            fontSize={12}
            tickLine={false}
            axisLine={false}
          />
          <YAxis
            stroke="#888888"
            fontSize={12}
            tickLine={false}
            axisLine={false}
            tickFormatter={(value) => `${value}`}
          />
          <Tooltip
            contentStyle={{
              backgroundColor: "hsl(var(--card))",
              borderRadius: "8px",
              border: "1px solid hsl(var(--border))",
            }}
            itemStyle={{ color: "hsl(var(--foreground))" }}
          />
          <Line
            type="monotone"
            dataKey="alerts"
            stroke="hsl(var(--primary))"
            strokeWidth={2}
            dot={false}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
