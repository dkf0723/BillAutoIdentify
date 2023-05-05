// import { useState } from "react"
import React, { useState, useEffect} from 'react';
import { Form, Link } from "react-router-dom"
import "./style.css"

import axios from 'axios';
import Account from '../Account/Account-index';
import { userinfo,userstat } from '../../global/databace';
//import './index.css' 寫法匯入index.css 下方引入 className=""
global.acc="0";
export  default function Login  (){
    
    const [loginaccount,setLoginAccount]=useState("");//帳號取得
    const [loginpassword,setLoginPassword]=useState("");//密碼取得
    const [access,setAccess] = useState("0");
    const [useridsave,setUseridsave] = useState("");

    //const [isLoading, setIsLoading] = useState(false);

    const Accounturl = "http://127.0.0.1:8080/bill-auto-identify/bill/all";//Account info link
    /*const [data, setData] = useState(null);
  useEffect(() => {
    axios.get('/api/data') // 發送 GET 請求到 Java Spring 後端的 /api/data 路由
      .then(response => {
        setData(response.data); // 更新狀態，將數據設置為響應數據
      })
      .catch(error => {
        console.error(error);
      });
  });*/

  //帳戶後端連接

  function checklogin(){
    fetch( Accounturl,{
        method:"GET",
       // mode: "no-cors",
        headers: {
            'Accept': 'application/json',
            'Access-Control-Allow-Origin': '*' ,
            'Content-Type': 'application/json',
        },
    })//選擇GET接收
    .then(response => {
        console.log(response)
        if (!response.ok) {
            throw new Error("HTTP error " + response.status);
        }
        return response.json();
    })
    .then(json => {
        //this.userID = json;
        console.log(json);
        for(var i=0 ;i<json.length;i++){
            var res = json[i];
            var useridres = res["userId"]
            var passwordres = res["password"]
            var companyres = res["company"]
            //var accpass = accountres+","+passwordres;
            console.log(useridres+","+passwordres+","+companyres);
            
            if(loginaccount === useridres && loginpassword === passwordres){
                alert("登入成功！ 歡迎"+useridres+"回來~");
                setAccess("1");
                setUseridsave(useridres);
                global.acc = loginaccount 
                window.location.href="/Account";
                break          
            }
            if(loginaccount ==="" && loginpassword === ""){
                alert("登入失敗！帳號及密碼沒有輸入喔！請正確輸入於欄位中~");
                break;
               }
            if(loginaccount !=="" || loginpassword !== ""){
                alert("登入失敗！請再次檢查帳號及密碼並重新輸入~");
                break;
            }
            
        }
    })
    .catch(e => {
        alert(e);
    })//^失敗動作
  }

///-------------

  function logout(){
    setAccess("0");
    setLoginAccount("");
    setLoginPassword("");
    alert("登出成功！"+useridsave+"期待下次相會");
  }
//---------------
/*
  const logindata = {Accunt:loginaccount,password:loginpassword};
  fetch( Accounturl,{
    method:"POST",//選擇POST發送
    headers: {
        'Accept': 'application/json',
        'Access-Control-Allow-Origin': '*' ,
        'Content-Type': 'application/json',//轉換json檔
    },
        body: JSON.stringify(logindata)//轉換文字檔
    })
    .then(res => {
        console.log(res)
        if (!res.ok) {
            throw new Error("HTTP error " + res.status);
        }
        return res.json();
    })
    .then(data => {
        console.log(data);
    })//^成功動作
    .catch(e => {
        alert(e);
    })//^失敗動作
*/
    
    /*function checklogin() {    
    if(loginaccount==="123"&&loginpassword==="123456"){
        alert('帳號'+loginaccount+'密碼'+loginpassword);
        window.location.href="/Account" //跳轉頁面
        }
    }*/
    if (access === "0"){
        return <div className="container">      
        <p>目前位置：Login</p>

        <table className="border">
            <tr>
            <td className="table-inside" colSpan={2}>登入</td>
            </tr>
            <tr>
                <td className="border" type="">帳號：</td>
                <td className="border">
                    <input type="text" defaultValue={loginaccount} placeholder="Email" 
                    onChange={(e)=>{setLoginAccount(e.target.value)}}></input>
                    內容:{loginaccount}
                </td>
            </tr>
            <tr>
                <td className="border">密碼：</td>
                <td className="border"><input type ="password" minLength={6} placeholder="6碼中英混和" 
                defaultValue={loginpassword} onChange={(e)=>{setLoginPassword(e.target.value)}}></input>
                內容:{loginpassword}
            </td>
            </tr>     
        </table>
        <p></p>
        <table>
            <tr>
                <td><Link to="/Password"><button>忘記密碼</button></Link></td>
                <td><Link to="/Signup"><button>前往註冊</button></Link></td>
                <td><input type="button" value="登入" onClick = {checklogin}/></td>
            </tr>
        </table>
    </div>
    }
    else{
        return <div className="container">      
        <p>目前位置：Logout</p>
                <td><input type="button" value="登出" onClick={logout}/></td>
            
    </div>
    }
    
    
}
    