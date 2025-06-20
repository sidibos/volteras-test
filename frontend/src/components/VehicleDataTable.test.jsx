import React from "react";
import { render, screen } from "@testing-library/react";
import VehicleDataTable from "./VehicleDataTable";

const mockData = [
  {
    id: 1,
    timestamp: "2025-06-19T10:00:00Z",
    speed: 40,
    odometer: 1200,
    soc: 80,
    elevation: 50,
    shift_state: "D",
  }
];

test("renders vehicle data rows", () => {
  render(<VehicleDataTable data={mockData} sortBy="speed" sortOrder="asc" handleSort={() => {}} />);
  expect(screen.getByText("40")).toBeInTheDocument();
  expect(screen.getByText("1200")).toBeInTheDocument();
  expect(screen.getByText("80")).toBeInTheDocument();
});
