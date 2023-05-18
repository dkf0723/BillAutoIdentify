import { useState } from "react"
import React from 'react';
import "./style.css"
import { Link } from "react-router-dom"
//import './index.css' 寫法匯入index.css 下方引入 className=""

export   default function MediaUpload  (){
    function upload(){
        const fileInput = document.getElementById('file-input');
        const file = fileInput.files[0];
        const formData = new FormData();
        formData.append('file', file);


        // 發送POST請求到API
        fetch('http://127.0.0.1:8080/bill-auto-identify/bill/upload', {
        method: 'POST',
        body: formData
        })
        .then(data => {
            // 處理API
            console.log(data);
            window.location.reload()
            alert("上傳成功！！")
            
        })
        .catch(error => {
            // 處理錯誤
            console.error(error);
        });
        }
    

    return <div className="container">       
        <p>目前位置：MediaUpload</p>
        <p>請選擇上傳要掃描的發票PDF檔案(可一次多檔)</p>
        <form action="" enctype="multipart/form-data">
            <input name="imgupload" type="file" id="file-input" accept=".pdf" multiple="multiple"></input>
        </form>
        <div>
            <p><Link to="/Media"><input type={"button"} value="圖檔送出，繼續上傳" name="upload" onClick={upload}></input></Link></p>
            <p><Link to="/Search"><input type={"button"} value="完成上傳，前往查詢頁"  name="uploadto" onClick={upload}></input></Link></p>
        </div>
    </div>
}

