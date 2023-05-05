import React, { useState } from 'react'
import { Form, Checkbox } from 'semantic-ui-react'
import { Link } from 'react-router-dom';

function SearchTable  ()  {
    const [value, setValue] = React.useState('this');//取得下拉選單的值
    const [daterange, setDaterange] = useState("");//發票期間取得
    const [invoicenumber, setInvoicenumber] = useState("")//發票號碼取得
    const [number, setNumber] = useState("")//統一編號取得

    function sendsearch(){
        global.pages = 0;
    }

    return <div>
            <table>
                <tr>
                <td>發票期間：</td>
                <td><input type="text" defaultValue={daterange} 
                    onChange={(e)=>{setDaterange(e.target.value)}} placeholder="例: 一一二年七、八月份"></input>
                </td>
                <td>發票號碼：</td>
                <td><input type="text" defaultValue={invoicenumber} onChange={(e)=>{setInvoicenumber(e.target.value)}} ></input></td>
                </tr>
                <tr>
                <td>統一編號：</td>
                <td><input type="text" defaultValue={number} onChange={(e)=>{setNumber(e.target.value)}}></input></td>
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
                        label='統編正確 則enable此選項'
                        name='checkboxRadioGroup'
                        value='查詢check有誤發票'
                        checked={value === '查詢check有誤發票'}
                        onChange={(e, data) => setValue(data.value)}
                    />
                </Form.Field>
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
            <Link to="/OutAndRevise"><input type="button" value="查詢" onClick = {sendsearch}/></Link>
    </div>
}

export default SearchTable