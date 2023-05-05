import { useState } from "react"
import React from 'react';
import { Link } from "react-router-dom"
import "./style.css"
import axios from 'axios';
//import './index.css' 寫法匯入index.css 下方引入 className=""

export   default function  ChangePswd (){
    const [oldpassword,setOldPassword]=useState(""); //原密碼取得
    const [newpassword,setNewPassword]=useState(""); //新密碼取得
    const [checkpassword,setCheckPassword]=useState(""); //再次輸入新密碼

    
    function savechange(){
        if(newpassword===checkpassword){
            alert("儲存成功");
        window.location.href="/Login" //跳轉頁面
        }
        else{
            alert("儲存失敗！新密碼不同！");
        }
        
    }

    return <div className="container">       
        <p>目前位置：ChangePassword</p>
        <table className="border">
            <tr>
            <td className="table-inside" colSpan={2}>修改密碼</td>
            </tr>
            <tr>
                <td className="border" colSpan={2}>忘記密碼者"原密碼"欄位填"臨時碼"</td>
            </tr>
            <tr>
                <td className="border">原密碼：</td>
                <td className="border">
                    <input type="password" defaultValue={oldpassword} placeholder="或臨時碼" 
                    onChange={(e)=>{setOldPassword(e.target.value)}} minLength={6}></input>
                    內容:{oldpassword}
                </td>
            </tr>
            <tr>
                <td className="border">新密碼：</td>
                <td className="border">
                    <input type="password" defaultValue={newpassword} placeholder="6碼中英混和" 
                    onChange={(e)=>{setNewPassword(e.target.value)}} minLength={6}></input>
                    內容:{newpassword}
                </td>  
            </tr>
            <tr>
                <td className="border">重複新密碼：</td>
                <td className="border">
                    <input type="password" defaultValue={checkpassword} placeholder="6碼中英混和" 
                    onChange={(e)=>{setCheckPassword(e.target.value)}} minLength={6}></input>
                    內容:{checkpassword}
                </td>
            </tr>
        </table>
        <p></p>
        <table>
            <tr>
                <td><Link to=""><button>取得臨時碼</button></Link></td>
                <td><Link to="/Login"><button>取消修改</button></Link></td>
                <td><input type="button" value="儲存修改" onClick = {savechange}/></td>
            </tr>
        </table>
    </div>
}