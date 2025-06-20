import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import VehicleFilterBar from "./VehicleFilterBar";

describe("VehicleFilterBar", () => {
  const mockFilter = jest.fn();
  const mockExport = jest.fn();
  const vehicleIds = ["123", "456"];

  beforeEach(() => {
    render(
      <VehicleFilterBar
        vehicleIds={vehicleIds}
        selectedVehicle=""
        startTime=""
        endTime=""
        setSelectedVehicle={() => {}}
        setStartTime={() => {}}
        setEndTime={() => {}}
        handleFilter={mockFilter}
        handleExport={mockExport}
      />
    );
  });

  it("renders vehicle dropdown and filter button", () => {
    expect(screen.getByText("Select Vehicle ID")).toBeInTheDocument();
    expect(screen.getByText("Filter")).toBeInTheDocument();
    expect(screen.getByText("Export As")).toBeInTheDocument();
  });
});
