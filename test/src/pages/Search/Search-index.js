import { useState } from "react"
import React from 'react';
import SearchTable from "./Search-Table";
import "./style.css"
import { Link } from "react-router-dom";
import { Input } from "semantic-ui-react";
//import './index.css' 寫法匯入index.css 下方引入 className=""

export   default function Search  (){

    

    return <div className="container">       
        <p>位置：Search</p>
        <h3 >查詢條件</h3>
        <div>
            <SearchTable />                
        </div>
        <div>
            <p><Link to="/Media"><button>前往圖檔上傳</button></Link></p>
        </div>
    </div>
}