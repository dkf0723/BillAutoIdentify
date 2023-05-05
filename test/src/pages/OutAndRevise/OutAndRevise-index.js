import { useState } from "react"
import React from 'react';
import OutAndReviseTable from "./OutAndRevise-Table";
import "./style.css"
//import './index.css' 寫法匯入index.css 下方引入 className=""

export   default function OutAndRevise  (){

    return <div className="container">       
        <p>位置：Search / OutAndRevise</p>
        <h3 >顯示</h3>
        <div>
            <OutAndReviseTable />                
        </div>
    </div>
}