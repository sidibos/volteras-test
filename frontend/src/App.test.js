import React from "react"; // ✅ required for JSX
import { render, screen } from "@testing-library/react";
import App from "./App";

test("renders learn react link", () => {
  render(<App />);
  const linkElement = screen.getByText(/Table of Vehicle Data/i);
  expect(linkElement).toBeInTheDocument();
});