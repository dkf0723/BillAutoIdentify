import React from "react";
import ReactDOM from "react-dom/client";
import "./styles.css";
import { LoadingSpinerComponent } from "./loadingSpinner";
import { Route, BrowserRouter, Routes, Link } from "react-router-dom";
import { routeConfig } from "./pages/router.js";
//常駐菜單列顯示
<link rel='icon' url="logo.ico"></link>
const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <BrowserRouter>
      <h1 className="logo" >Invoice EQC</h1>
      <hr />
      <div className="banner_button">
        <Link to="/Home" className="abc">Home</Link>
        <Link to="/Search" className="abc">Search</Link>
        <Link to="/Media" className="abc">Media</Link>
        <Link to="/Account" className="abc">Account</Link>
        <Link to="/Login" className="abc">Login/Signup</Link>
      </div>
      <br />
      <hr />
      <LoadingSpinerComponent />
      <Routes>
        {routeConfig.map((router) => (
          <>
            <Route exact element={router.element} path={router.path} />
          </>
        ))}
      </Routes>
      <br />
      <div className="foot">
        資料安全說明 | 隱私權聲明 | 國立臺北商業大學版權所有
        <br />
        地址 : 台北市中正區濟南路一段321號
        <br />
        上班時間 : 星期一至星期五 上午08:30~12:30下午1:30~5:30 （服務時間）
        <br />
        電話 : (02)3322-2777; E-mail信箱 : 10946018@ntub.edu.tw
        <br />
        Copyright© 北商112405發票管理平台專題 版權所有
      </div>
      <div className="mar">
        <marquee direction="right" height="30" scrollamount="5" behavior="alternate">內容尚未確定</marquee>
      </div>
    </BrowserRouter>
  </React.StrictMode>
);