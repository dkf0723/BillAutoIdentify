import { useState } from "react"
import React from 'react';
import "./style.css"
import { Link } from "react-router-dom"
//import { userinfoo } from "../Login/Login-index";
//import './index.css' 寫法匯入index.css 下方引入 className=""
//import { userinfo } from "../../global/databace";

export   default function Account  (){
    //const username = userinfoo.userid
    var username = global.acc;
    //var username = userinfo.userid;
    const [printaccount,setPrintAccount]=useState("xxxxx@gmail.com");//值填入帳號欄
    const [printusername,setPrintUsername]=useState(username); //值填入使用者名稱欄
    const [printcompany,setPrintCompany]=useState("cc事務所公司"); //值填入公司欄


    
    return <div className="container">       
        <p>目前位置：Account</p>
        <table className="border">
            <tr>
            <td className="table-inside" colSpan={2}>帳號資訊</td>
            </tr>
            
            <tr>
                <td className="border">帳號：</td>
                <td className="border"><input type="text" defaultValue={printaccount} 
                    onChange={(e)=>{setPrintAccount(e.target.value)}}></input>
                </td>
                
            </tr>
            <tr>
                <td className="border">密碼：</td>
                <td className="border"><Link to="/Password">修改密碼</Link></td>
            </tr>
            <tr>
                <td className="border">使用者名稱：</td>
                <td className="border"><input type="text" defaultValue={printusername} 
                    onChange={(e)=>{setPrintUsername(e.target.value)}}></input>
                </td>
                
            </tr>
            <tr>
                <td className="border">公司名稱：</td>
                <td className="border"><input type="text" defaultValue={printcompany}
                    onChange={(e)=>{setPrintCompany(e.target.value)}}></input>
                </td>
                
            </tr>
        </table>
        <p></p>
        <div>
            <Link to="/Login"><button>"提示.沒有內容" 請前往登入頁</button></Link>
            
        </div>
    </div>
}
