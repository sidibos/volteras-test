import React from "react";
import { render } from "@testing-library/react";
import VehicleDataChart from "./VehicleDataChart";

const data = [
  {
    timestamp: "2025-06-19T10:00:00Z",
    speed: 30,
    soc: 90
  }
];

test("renders chart heading", () => {
  const { getByText } = render(<VehicleDataChart data={data} />);
  expect(getByText("Vehicle Data Chart")).toBeInTheDocument();
});