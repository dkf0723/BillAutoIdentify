import { useState } from "react"
import React from 'react';
import { Link } from "react-router-dom"
import "./style.css"

//import './index.css' 寫法匯入index.css 下方引入 className=""

export   default function Signup  (){
    
    return <div className="container">       
        <p>目前位置：Singup</p>
        <table className="border">
            <tr>
            <td className="table-inside" colSpan={2}>註冊</td>
            </tr>
            <tr>
                <td className="border">帳號：</td>
                <td className="border"><input type="email" placeholder="E-mail"></input></td>
            </tr>
            <tr>
                <td className="border">密碼：</td>
                <td className="border"><input type="password" minLength={6} placeholder="6碼中英混和"></input></td>
            </tr>
            <tr>
                <td className="border">再次輸入密碼：</td>
                <td className="border"><input type="password" minLength={6} placeholder="6碼中英混和"></input></td>
            </tr>
            <tr>
                <td className="border">使用者名稱：</td>
                <td className="border"><input placeholder="陳xx"></input></td>
            </tr>
            <tr>
                <td className="border">公司名稱：</td>
                <td className="border"><input placeholder="xx公司"></input></td>
            </tr>
        </table>
        <p></p>
        <table>
            <tr>
                <td><Link to="/Login"><button>返回登入</button></Link></td>
                <td><Link to="/Password"><button>忘記密碼</button></Link></td>
                <td><Link to="/Login"><button>送出註冊</button></Link></td>
            </tr>
        </table>
    </div>
}