import React, { useEffect, useState } from "react";
import {
  Container,
  Navbar,
  Row,
  Col,
  Table,
  Form,
  Button,
  Card,
  Pagination,
  Dropdown, 
  DropdownButton
} from "react-bootstrap";
import axios from "axios";
import dayjs from "dayjs";
import {
    LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer
} from "recharts";

import VehicleFilterBar from "./components/VehicleFilterBar";
import VehicleDataTable from "./components/VehicleDataTable";
import VehicleDataChart from "./components/VehicleDataChart";

const PAGE_SIZE = 40;

const VehicleDataPage = () => {
  const [vehicleIds, setVehicleIds] = useState([]);
  const [selectedVehicle, setSelectedVehicle] = useState("");
  const [startTime, setStartTime] = useState("");
  const [endTime, setEndTime] = useState("");
  const [data, setData] = useState([]);
  const [page, setPage] = useState(0);
  //const [total, setTotal] = useState(0);
  //const [totalCount, setTotalCount] = useState(0);
  const [totalPages, setTotalPages] = useState(0);
  const [sortBy, setSortBy] = useState("timestamp");
  const [sortOrder, setSortOrder] = useState("asc");

  // Get all unique vehicle_ids (can be a dedicated API if needed)
  const fetchVehicleIds = async () => {
    const res = await axios.get(`${process.env.REACT_APP_API_BASE}/vehicles`);
    const unique = [...new Set(res.data.map((d) => d.vehicle_id))];
    setVehicleIds(unique);
  };

  const fetchVehicleData = async () => {
    if (!selectedVehicle) return;

    const params = {
      vehicle_id: selectedVehicle,
      skip: page * PAGE_SIZE,
      limit: PAGE_SIZE,
    };

    if (startTime) params.start = startTime;
    if (endTime) params.end = endTime;

    const res = await axios.get(`${process.env.REACT_APP_API_BASE}/vehicle_data/`, { params });
    setData(res.data);

    // 2. Fetch total count (for pagination)
    const countParams = {
        vehicle_id: selectedVehicle,
    };
    if (startTime) countParams.start = startTime;
    if (endTime) countParams.end = endTime;

    const countRes = await axios.get(`${process.env.REACT_APP_API_BASE}/vehicle_data/count`, { params: countParams });
    const count = countRes.data;
    setTotalPages(Math.ceil(count / PAGE_SIZE));
  };

  useEffect(() => {
    fetchVehicleIds();
  }, []);

  useEffect(() => {
    fetchVehicleData();
  },[page]);

  const handleFilter = () => {
    setPage(0);
    fetchVehicleData();
  };

  const handleExport = (format) => {
    if (!selectedVehicle) {
        alert("Please select a vehicle to export.");
        return;
    }

    const params = new URLSearchParams({
      vehicle_id: selectedVehicle,
      format,
    });
    if (startTime) params.append("start", startTime);
    if (endTime) params.append("end", endTime);
  
    const url = `${process.env.REACT_APP_API_BASE}/vehicle_data/export?${params.toString()}`;
  
    // Trigger file download
    window.open(url, "_blank");
  };

  const handleSort = (column) => {
    if (sortBy === column) {
      setSortOrder((prev) => (prev === "asc" ? "desc" : "asc"));
    } else {
      setSortBy(column);
      setSortOrder("asc");
    }
  };

  const sortedData = [...data].sort((a, b) => {
    const aVal = a[sortBy];
    const bVal = b[sortBy];
  
    // Handle null/undefined
    if (aVal == null) return 1;
    if (bVal == null) return -1;
  
    if (typeof aVal === "string") {
      return sortOrder === "asc"
        ? aVal.localeCompare(bVal)
        : bVal.localeCompare(aVal);
    }
  
    return sortOrder === "asc" ? aVal - bVal : bVal - aVal;
  });

  return (
    <div>
      {/* Top Navbar */}
      <Card className="text-center p-5">
        <Card.Body>
            <Card.Text className="h3 text-uppercase text-info font-weight-bold">
                Table of Vehicle Data
            </Card.Text>
        </Card.Body>
      </Card>

      <VehicleFilterBar
        vehicleIds={vehicleIds}
        selectedVehicle={selectedVehicle}
        startTime={startTime}
        endTime={endTime}
        setSelectedVehicle={setSelectedVehicle}
        setStartTime={setStartTime}
        setEndTime={setEndTime}
        handleFilter={handleFilter}
        handleExport={handleExport}
      />

      <Container className="mt-4">
        <VehicleDataTable
          data={sortedData}
          sortBy={sortBy}
          sortOrder={sortOrder}
          handleSort={handleSort}
      />

        <VehicleDataChart data={sortedData} />

        {/* Pagination */}
        <div className="d-flex justify-content-end">
          <Pagination>
            <Pagination.Prev onClick={() => setPage((p) => Math.max(p - 1, 0))} disabled={page === 0} />
            {Array.from({ length: totalPages }, (_, i) => (
              <Pagination.Item key={i} active={i === page} onClick={() => setPage(i)}>
                {i + 1}
              </Pagination.Item>
            ))}
            <Pagination.Next onClick={() => setPage((p) => Math.min(p + 1, totalPages - 1))} disabled={page >= totalPages - 1} />
          </Pagination>
        </div>
      </Container>
    </div>
  );
};

export default VehicleDataPage;
