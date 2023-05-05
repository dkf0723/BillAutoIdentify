import { useState } from "react"
import React from 'react';
import "./style.css"
import { Link } from "react-router-dom"
//import './index.css' 寫法匯入index.css 下方引入 className=""

export   default function MediaUpload  (){

    return <div className="container">       
        <p>目前位置：MediaUpload</p>
        <p>請選擇上傳要掃描的發票PDF檔案(可一次多檔)</p>
        <form action="" enctype="multipart/form-data">
            <input name="imgupload" type="file" accept=".pdf" multiple="multiple"></input>
        </form>
        <div>
            <p><Link to="/Media"><input type={"submit"} value="圖檔送出，繼續上傳" name="upload"></input></Link></p>
            <p><Link to="/Search"><input type={"submit"} value="完成上傳，前往查詢頁"  name="upload"></input></Link></p>
        </div>
    </div>
}

