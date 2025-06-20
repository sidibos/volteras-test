import React from "react";
import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  CartesianGrid
} from "recharts";
import dayjs from "dayjs";

const VehicleDataChart = ({ data }) => {
  if (!data || data.length === 0) return null;

  return (
    <>
      <h5 className="mt-4">Vehicle Data Chart</h5>
      <ResponsiveContainer width="100%" height={400}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="timestamp" tickFormatter={(v) => dayjs(v).format("HH:mm")} />
          <YAxis yAxisId="left" label={{ value: "Speed (km/h)", angle: -90, position: "insideLeft" }} />
          <YAxis
            yAxisId="right"
            orientation="right"
            label={{ value: "SOC (%)", angle: -90, position: "insideRight" }}
          />
          <Tooltip />
          <Legend />
          <Line yAxisId="left" type="monotone" dataKey="speed" stroke="#8884d8" name="Speed" dot={false} />
          <Line yAxisId="right" type="monotone" dataKey="soc" stroke="#82ca9d" name="SOC" dot={false} />
        </LineChart>
      </ResponsiveContainer>
    </>
  );
};

export default VehicleDataChart;