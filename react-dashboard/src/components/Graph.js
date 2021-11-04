import React from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";
import "./Graph.css";

const Graph = ({ data }) => {
  const real = data.real;
  const predicted = data.predicted;
  const date = data.date.map((d) => new Date(d).toLocaleDateString());
  //   console.log(date["0"]);
  const data_mapped = [];

  for (let i = 0; i < date.length; i++) {
    if (i < 60)
      data_mapped.push({ real: real[i], predicted: null, date: date[i] });
    else
      data_mapped.push({
        real: real[i],
        predicted: predicted[i - 60],
        date: date[i],
      });
  }

  //   const date_new = date[0].split(" ");
  //   console.log(date);
  // console.log(date_new[1] + " " + date_new[2] + " " + date_new[3]);

  return (
    <div className="graph-container">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart
          width={500}
          height={300}
          data={data_mapped}
          margin={{
            top: 5,
            right: 30,
            left: 20,
            bottom: 5,
          }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="date" minTickGap={40} />
          <YAxis />
          <Tooltip />
          <Legend verticalAlign="top" height={36} />
          <Line type="monotone" dataKey="real" stroke="#b91c65" dot={false} />
          <Line
            type="monotone"
            dataKey="predicted"
            stroke="#10309c"
            dot={false}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default Graph;
