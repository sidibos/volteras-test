import React from "react";
import { Navbar, Container, Row, Col, Form, Button, DropdownButton, Dropdown } from "react-bootstrap";

const VehicleFilterBar = ({
  vehicleIds,
  selectedVehicle,
  startTime,
  endTime,
  setSelectedVehicle,
  setStartTime,
  setEndTime,
  handleFilter,
  handleExport
}) => (
  <Navbar bg="light" className="px-3 py-2 shadow-sm">
    <Container fluid>
      <Row className="w-100 align-items-center">
        <Col md={3}>
          <Form.Select value={selectedVehicle} onChange={(e) => setSelectedVehicle(e.target.value)}>
            <option value="">Select Vehicle ID</option>
            {vehicleIds.map((id) => (
              <option key={id} value={id}>
                {id}
              </option>
            ))}
          </Form.Select>
        </Col>
        <Col md={3}>
          <Form.Control
            type="datetime-local"
            value={startTime}
            onChange={(e) => setStartTime(e.target.value)}
          />
        </Col>
        <Col md={3}>
          <Form.Control
            type="datetime-local"
            value={endTime}
            onChange={(e) => setEndTime(e.target.value)}
          />
        </Col>
        <Col md={3} className="ms-auto d-flex justify-content-end gap-2">
          <Button onClick={handleFilter} className="me-1">
            Filter
          </Button>
          <DropdownButton
            id="export-dropdown"
            title="Export As"
            className="me-2"
            variant="secondary"
            onSelect={handleExport}
          >
            <Dropdown.Item eventKey="csv">CSV</Dropdown.Item>
            <Dropdown.Item eventKey="json">JSON</Dropdown.Item>
            <Dropdown.Item eventKey="excel">Excel</Dropdown.Item>
          </DropdownButton>
        </Col>
      </Row>
    </Container>
  </Navbar>
);

export default VehicleFilterBar;