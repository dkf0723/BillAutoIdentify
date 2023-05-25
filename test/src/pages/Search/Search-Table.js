import React, { useState } from 'react'
import { Form, Checkbox } from 'semantic-ui-react'
import { Link } from 'react-router-dom';
import { Checkdata } from '../OutAndRevise/checkdata';
global.company = "";
function SearchTable() {
    const [value, setValue] = React.useState('this');//取得下拉選單的值
    const [daterange, setDaterange] = useState("");//發票期間取得
    const [invoicenumber, setInvoicenumber] = useState("")//發票號碼取得
    const [number, setNumber] = useState("")//統一編號取得

    function sendsearch() {
        global.pages = 0;
    }
    const handleInput = (e) => {
        console.log(e.target.value)
        /*const numbervalue = document.getElementById("checknumber").value;
        if (numbervalue !== "" && numbervalue.length === 8) {
            //Checkdata();

            const url = ("https://eip.fia.gov.tw/OAI/api/businessRegistration/" + numbervalue);
            console.log(url)
            fetch(url, {
                method: "GET",
                headers: {
                    'Accept': 'application/json',
                    'Access-Control-Allow-Origin': '*',
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
                .then(info => {
                    //const companyname  = info;
                    //console.log(info)
                })
                .catch(e => {
                    alert(e);
                })//^失敗動作
        }*/
    }


    return <div>
        <table>
            <tr>
                <td>發票期間：</td>
                <td>
                    <select onChange={(e) => handleInput(e)}>
                        <option value="一一二年一、二月份">一一二年一、二月份</option>
                        <option value="一一二年三、四月份">一一二年三、四月份</option>
                        <option value="一一二年五、六月份">一一二年五、六月份</option>
                        <option value="一一二年七、八月份">一一二年七、八月份</option>
                        <option value="一一二年九、十月份">一一二年九、十月份</option>
                        <option value="一一二年十一、十二月份">一一二年十一、十二月份</option>
                    </select>
                </td>
                <td>發票號碼：</td>
                <td><input type="text" defaultValue={invoicenumber} onChange={(e) => { setInvoicenumber(e.target.value) }} ></input></td>
            </tr>
            <tr>
                <td>統一編號：</td>
                <td><input type="text" defaultValue={number} onChange={(e) => handleInput(e)} id='checknumber' maxLength={8}></input></td>
            </tr>

            <tr><p></p></tr>
            <tr>
                <td>發票狀態：</td>
            </tr>
        </table>
        <Form>
            <Form.Field>
                <Checkbox
                    radio
                    label='查詢check無誤發票'
                    name='checkboxRadioGroup'
                    value='查詢check無誤發票'
                    checked={value === '查詢check無誤發票'}
                    onChange={(e, data) => setValue(data.value)}
                />
            </Form.Field>
            <Form.Field>
                <Checkbox
                    radio
                    label='查詢人工修正發票'
                    name='checkboxRadioGroup'
                    value='查詢人工修正發票'
                    checked={value === '查詢人工修正發票'}
                    onChange={(e, data) => setValue(data.value)}
                />
            </Form.Field>
        </Form>
        <div><p></p></div>
        <Link to="/OutAndRevise"><input type="button" value="查詢" onClick={sendsearch} /></Link>
    </div>
}

export default SearchTable