import React from "react";
import { Table } from "react-bootstrap";
import dayjs from "dayjs";

const VehicleDataTable = ({ data, sortBy, sortOrder, handleSort }) => {
  return (
    <Table striped bordered hover responsive>
      <thead>
        <tr>
          {["timestamp", "speed", "odometer", "soc", "elevation", "shift_state"].map((col) => (
            <th key={col} onClick={() => handleSort(col)} style={{ cursor: "pointer" }}>
              {col.charAt(0).toUpperCase() + col.slice(1).replace("_", " ")}
              {sortBy === col && (sortOrder === "asc" ? " ↑" : " ↓")}
            </th>
          ))}
        </tr>
      </thead>
      <tbody>
        {data.length > 0 ? (
          data.map((row) => (
            <tr key={row.id}>
              <td>{dayjs(row.timestamp).format("YYYY-MM-DD HH:mm:ss")}</td>
              <td>{row.speed ?? "-"}</td>
              <td>{row.odometer}</td>
              <td>{row.soc}</td>
              <td>{row.elevation}</td>
              <td>{row.shift_state ?? "-"}</td>
            </tr>
          ))
        ) : (
          <tr>
            <td colSpan="6" className="text-center">
              No data found
            </td>
          </tr>
        )}
      </tbody>
    </Table>
  );
};

export default VehicleDataTable;