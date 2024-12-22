import React from "react";
import ReactDOM from "react-dom/client"; // Corrected the import here

const parent = React.createElement("h1", { id: "heading" }, "Hello Om!");

const root = ReactDOM.createRoot(document.getElementById("root"));

root.render(parent);
