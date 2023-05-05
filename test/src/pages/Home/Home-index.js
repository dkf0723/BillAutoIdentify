import { useState } from "react"
import React from 'react';
import "./style.css"
import Edit from "./Edit"
import List from "./List"
import Itim from "./Item"
//import './index.css' 寫法匯入index.css 下方引入 className=""

export   default function Home  (){
    
    //const [data,setData] = useState(100)
    //function plus() {
        //setA(function(prev){
            //return prev + 200
        //})
    //}{data}<button onClick={plus}>加法</button>

    return <div className="container">
        
        <Edit />
        <List />
        <Itim />
    </div>
}

//export default Home