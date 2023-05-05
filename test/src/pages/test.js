import React from 'react';
import { trackPromise} from 'react-promise-tracker';
import "./style.css"

 export default function Test() {

 
        return(<div className='container'><button className="square" onClick={function(){send()}}>
        button
      </button></div>)
    
}

function send(){
    trackPromise(
        fetch('https://jsonplaceholder.typicode.com/todos/1')
        .then(response => response.json())
        .then(json => console.log(json))
    )
    }
