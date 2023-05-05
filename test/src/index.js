import React from "react";
import ReactDOM from "react-dom/client";
import "./styles.css";
import { LoadingSpinerComponent } from "./loadingSpinner";
import { Route, BrowserRouter, Routes, Link } from "react-router-dom";
import { routeConfig } from "./pages/router.js";
//常駐菜單列顯示
const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <BrowserRouter>
      <div className="container">
        <h1>發票IN</h1>
        <div className="banner_button">
          {" "}
          <Link to="/">Home</Link>
        </div>
        <div className="banner_button">
          {" "}
          <Link to="/Search">Search</Link>
        </div>
        <div className="banner_button">
          {" "}
          <Link to="/Media">Media</Link>
        </div>
        <div className="banner_button">
          {" "}
          <Link to="/Account">Account</Link>
        </div>
        <div className="banner_button">
          {" "}
          <Link to="/Login">Login/Signup</Link>
        </div>
      </div>
      
      <Routes>
        {routeConfig.map((router) => (
          <>
            <Route exact element={router.element} path={router.path} />
          </>
        ))}
      </Routes>
    </BrowserRouter>
  </React.StrictMode>
);