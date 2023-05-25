import React, { useState, useEffect } from 'react'
import { Form, Checkbox, Button, Loader } from 'semantic-ui-react'
import "./style.css";
import { Link } from "react-router-dom";
import { Checkdata } from './checkdata';
import { setup } from './setup';

export function OutAndReviseTable() {
    //-----------

    const [resData, setResData] = useState([]);//陣列-api json in
    const [value1, setValue1] = useState('this')//取得下拉選單的值(稅別)
    const [value2, setValue2] = useState('this')//取得下拉選單的值(建檔與否)
    const [pageload, setPageload] = useState(global.pages);
    const [, updateState] = useState("");
    //----------------
    const [datetime, setDatetime] = useState("");//日期
    const [blockletter, setBlockletter] = useState("")//新台幣大寫
    const [daterevise, setDaterevise] = useState("yyyy/mm/dd hh:mm:ss")//修改時間
    const [inspector, setInspector] = useState("王大明")//修改人員
    const [totalpage, setTotalpage] = useState("幾")//總張數


    const [invoicenumber, setInvoicenumber] = useState("")//發票號碼
    const [invoicetype, setInvoicetype] = useState("")//發票二三聯
    const [daterange, setDaterange] = useState("");//發票期間
    const [number, setNumber] = useState("")//統一編號

    const [buyer, setBuyer] = useState("");//買受人
    const [address, setAddress] = useState("")//地址

    const [r1c1, setR1C1] = useState("")//第一欄欄位
    const [r1c2, setR1C2] = useState("")//第一欄欄位
    const [r1c3, setR1C3] = useState("")//第一欄欄位
    const [r1c4, setR1C4] = useState("")//第一欄欄位
    const [r1c5, setR1C5] = useState("")//第一欄欄位

    const [r2c1, setR2C1] = useState(0)//第二欄欄位
    const [r2c2, setR2C2] = useState(0)//第二欄欄位
    const [r2c3, setR2C3] = useState(0)//第二欄欄位
    const [r2c4, setR2C4] = useState(0)//第二欄欄位
    const [r2c5, setR2C5] = useState(0)//第二欄欄位

    const [r3c1, setR3C1] = useState(0)//第三欄欄位
    const [r3c2, setR3C2] = useState(0)//第三欄欄位
    const [r3c3, setR3C3] = useState(0)//第三欄欄位
    const [r3c4, setR3C4] = useState(0)//第三欄欄位
    const [r3c5, setR3C5] = useState(0)//第三欄欄位

    const [r4c1, setR4C1] = useState(0)//第四欄欄位
    const [r4c2, setR4C2] = useState(0)//第四欄欄位
    const [r4c3, setR4C3] = useState(0)//第四欄欄位
    const [r4c4, setR4C4] = useState(0)//第四欄欄位
    const [r4c5, setR4C5] = useState(0)//第四欄欄位

    const [totalmini, setTotalmini] = useState("")//合計
    const [tax, setTax] = useState("")//稅額
    const [totalall, setTotalall] = useState("")//總計 

    const [insidepage, setInsidepage] = useState("")//目前張數


    //if(page!== global.pages){OutAndReviseTable()}
    useEffect(() => {
        pageset();
        Checkdata();
    }, [resData.billNumber]);

    const pageset = () => {
        var page = global.pages;
        var s = { page };
        const invoicen = "http://127.0.0.1:8080/bill-auto-identify/bill/check";//Account info link
        fetch(invoicen, {
            /*method: "GET",
            headers: {
                'Accept': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json',
            },*/
            method: "post",//選擇POST發送
            headers: {
                'Accept': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json',//轉換json檔
            },
            body: JSON.stringify(s)
        })//選擇GET接收
            .then(response => {
                console.log(response)
                if (!response.ok) {
                    throw new Error("HTTP error " + response.status);
                }
                return response.json();
            })
            .then(info => {
                /*if(info["billDetailList"].length<5){
                    const i =  5-info["billDetailList"].length;
                    for(i;i){

                    }
                    info["billDetailList"].push("{number: 'MK56758388', column: 1, productName: '文件匣', price: 80, amount: 10, …}")
                }*/
                setResData(info);
                setValue1(info["taxType"]);
                console.log(info);
                //日期格式

                var date = info["dateTime"]
                setDatetime(date[0] + "年 " + date[1] + "月 " + date[2] + "日");

                setDaterevise(info["includeDateTime"].substr(0, 4) + "年 " +
                    info["includeDateTime"].substr(5, 2) +
                    "月 " + info["includeDateTime"].substr(8, 2) + "日 " +
                    info["includeDateTime"].substr(-10, 8));//日期
                Checkdata();
            })
            .catch(e => {
                alert(e);
            })//^失敗動作
    }
    //---------------------------------
    global.taxbox = value1;
    global.data = JSON.parse(JSON.stringify(resData))
    //alert(JSON.stringify(resData));
    function upj() {
        //alert("上一頁");
        if (global.pages >= 1) {
            global.pages -= 1;
            setPageload(global.pages);
            setResData([]);
            pageset();
            //alert(global.pages)
        }
        //alert(global.setnew)
    }
    function downj() {
        //alert("下一頁");
        //var pagedown = { page: 1 };
        global.pages += 1;
        setPageload(global.pages);
        setResData([]);
        pageset();

        //alert(global.pages)
        //alert(pageload);
        //setup();
        /*fetch(invoicen,{
            method:"POST",//選擇POST發送
            headers: {
                'Accept': 'application/json',
                'Access-Control-Allow-Origin': '*' ,
                'Content-Type': 'application/json',//轉換json檔
            },
            body: JSON.stringify(pagedown)
                       
            })
            .then(res => {
                console.log(res)
                if (!res.ok) {
                    throw new Error("HTTP error " + res.status);
                }
                return res.json();
            })*/

    }

    /*function normal(){
        const totalid = ["checkinvoicenumber"];
        for(const i=0; i<totalid.length; i++){
            document.getElementById(totalall[i]).style.color="red";//文字原色
        } 
    }*/
    function giveupchange() {
        alert("放棄修改");
    }

    const handleInput = (e) => {
        Checkdata();
        console.log(e.target.value)
    }

    function addnum() {

    }


    return downj.s, <div>
        <table>
            <tr>
                <td>發票號碼：</td>
                <td><input type="text" Value={resData.billNumber} onChange={(e) => handleInput(e)} placeholder="(2碼大寫英文8碼數字)" maxLength={10} id="checkinvoicenumber"></input></td>
                <td>發票二聯/三聯：</td>
                <td><input type="text" Value={resData.billType} onChange={(e) => handleInput(e)} placeholder="(2~4字元)" minLength={2} maxLength={4} id="checkinvoicetype"></input></td>
            </tr>

            <tr>
                <td>發票期間：</td>
                <td><input type="text" defaultValue={resData.yearMonth} onChange={(e) => handleInput(e)} id="checkdaterange"></input></td>
            </tr>

            <tr>
                <td>統一編號：</td>
                <td><input type="text" defaultValue={resData.taxIdNumber} onChange={(e) => handleInput(e)} placeholder="(8碼)" maxLength={8} id="checknumber"></input></td>
                <td className='table-right'>日期：</td>
                <td><input type="text" defaultValue={datetime} onChange={(e) => handleInput(e)} id="checkdatetime"></input></td>
            </tr>

            <tr>
                <td>買受人：</td>
                <td><input type="text" defaultValue={resData.buyer} onChange={(e) => handleInput(e)} placeholder="(最低2字元)" minLength={2} id="checkbuyer"></input></td>

            </tr>
            <tr>
                <td>地址：</td>
                <td><input type="text" defaultValue={resData.address} onChange={(e) => handleInput(e)} colSpan={2} id="checkaddress"></input></td>
            </tr>
        </table>
        <table className='border'>
            <tr className='table-inside'>
                <td className='border' id="">項次</td>
                <td className='border' id="">品名</td>
                <td className='border' id="">數量</td>
                <td className='border' id="">單價</td>
                <td className='border' id="">金額</td>
            </tr>
            {resData.billDetailList &&
                resData.billDetailList.map((data, index) =>
                    <tr className='table-inside' key={index}>
                        <td>{index + 1}</td>
                        <td className='border'><input type="text" defaultValue={data.productName} onChange={(e) => handleInput(e)} placeholder="r1" id={"r1c" + (index + 1)}></input></td>
                        <td className='border'><input type="number" className='textright' defaultValue={data.amount} onChange={(e) => handleInput(e)} placeholder="r2" id={"r2c" + (index + 1)} /></td>
                        <td className='border'><input type="number" className='textright' defaultValue={data.price} onChange={(e) => handleInput(e)} placeholder="r3" id={"r3c" + (index + 1)} /></td>
                        <td className='border'><input type="number" className='textright' defaultValue={data.totalColumnPrice} onChange={(e) => handleInput(e)} placeholder="r4" id={"r4c" + (index + 1)} /></td>
                    </tr>
                )
            }

            {/* <tr className='table-inside'>
                <td className='border'>1</td>
                <td className='border'><input type="text" defaultValue={r1c1} onChange={(e) => { setR1C1(e.target.value) }} placeholder="r1c1" id="r1c1"></input></td>
                <td className='border'><input type="number" className='textright' defaultValue={r2c1} onChange={(e) => { setR2C1(e.target.value) }} placeholder="r2c1" id="r2c1"></input></td>
                <td className='border'><input type="number" className='textright' defaultValue={r3c1} onChange={(e) => { setR3C1(e.target.value) }} placeholder="r3c1" id="r3c1"></input></td>
                <td className='border'><input type="number" className='textright' defaultValue={r4c1} onChange={(e) => { setR4C1(e.target.value) }} placeholder="r4c1" id="r4c1"></input></td>
            </tr>

            <tr className='table-inside'>
                <td className='border'>2</td>
                <td className='border'><input type="text" defaultValue={r1c2} onChange={(e) => { setR1C2(e.target.value) }} placeholder="r1c2" id="r1c2"></input></td>
                <td className='border'><input type="number" className='textright' defaultValue={r2c2} onChange={(e) => { setR2C2(e.target.value) }} placeholder="r2c2" id="r2c2"></input></td>
                <td className='border'><input type="number" className='textright' defaultValue={r3c2} onChange={(e) => { setR3C2(e.target.value) }} placeholder="r3c2" id="r3c2"></input></td>
                <td className='border'><input type="number" className='textright' defaultValue={r4c2} onChange={(e) => { setR4C2(e.target.value) }} placeholder="r4c2" id="r4c2"></input></td>
            </tr>

            <tr className='table-inside'>
                <td className='border'>3</td>
                <td className='border'><input type="text" defaultValue={r1c3} onChange={(e) => { setR1C3(e.target.value) }} placeholder="r1c3" id="r1c3"></input></td>
                <td className='border'><input type="number" className='textright' defaultValue={r2c3} onChange={(e) => { setR2C3(e.target.value) }} placeholder="r2c3" id="r2c3"></input></td>
                <td className='border'><input type="number" className='textright' defaultValue={r3c3} onChange={(e) => { setR3C3(e.target.value) }} placeholder="r3c3" id="r3c3"></input></td>
                <td className='border'><input type="number" className='textright' defaultValue={r4c3} onChange={(e) => { setR4C3(e.target.value) }} placeholder="r4c3" id="r4c3"></input></td>
            </tr>

            <tr className='table-inside'>
                <td className='border'>4</td>
                <td className='border'><input type="text" defaultValue={r1c4} onChange={(e) => { setR1C4(e.target.value) }} placeholder="r1c4" id="r1c4"></input></td>
                <td className='border'><input type="number" className='textright' defaultValue={r2c4} onChange={(e) => { setR2C4(e.target.value) }} placeholder="r2c4" id="r2c4"></input></td>
                <td className='border'><input type="number" className='textright' defaultValue={r3c4} onChange={(e) => { setR3C4(e.target.value) }} placeholder="r3c4" id="r3c4"></input></td>
                <td className='border'><input type="number" className='textright' defaultValue={r4c4} onChange={(e) => { setR4C4(e.target.value) }} placeholder="r4c4" id="r4c4"></input></td>
            </tr>

            <tr className='table-inside'>
                <td className='border'>5</td>
                <td className='border'><input type="text" defaultValue={r1c5} onChange={(e) => { setR1C5(e.target.value) }} placeholder="r1c5" id="r1c5"></input></td>
                <td className='border'><input type="number" className='textright' defaultValue={r2c5} onChange={(e) => { setR2C5(e.target.value) }} placeholder="r2c5" id="r2c5"></input></td>
                <td className='border'><input type="number" className='textright' defaultValue={r3c5} onChange={(e) => { setR3C5(e.target.value) }} placeholder="r3c5" id="r3c5"></input></td>
                <td className='border'><input type="number" className='textright' defaultValue={r4c5} onChange={(e) => { setR4C5(e.target.value) }} placeholder="r4c5" id="r4c5"></input></td>
            </tr> */}

            <tr className='border'>
                <td className='table-right-border' colSpan={4}>合計</td>
                <td><input type="number" className='textright' defaultValue={resData.total} onChange={(e) => handleInput(e)} id="checktotalmini"></input></td>
            </tr>


            <tr>

                <td className='table-right-border' rowSpan={2} colSpan={2}>營業稅：</td>
                <td rowSpan={2}>
                    <Form defaultValue={resData.taxType}>
                        <Form.Field>
                            <Checkbox
                                radio
                                label='應稅'
                                name='checkboxRadioGroup'
                                valuechange1='應稅'
                                checked={value1 === '應稅'}
                                onChange={(e, data1) => setValue1('應稅')}
                            />
                        </Form.Field>
                        <Form.Field>
                            <Checkbox
                                radio
                                label='零稅率'
                                name='checkboxRadioGroup'
                                valuechange1='零稅率'
                                checked={value1 === '零稅率'}
                                onChange={(e, data1) => setValue1('零稅率')}

                            />
                        </Form.Field>
                        <Form.Field>
                            <Checkbox
                                radio
                                label='免稅'
                                name='checkboxRadioGroup'
                                valuechange1='免稅'
                                checked={value1 === '免稅'}
                                onChange={(e, data1) => setValue1('免稅')}
                            />
                        </Form.Field>
                    </Form>
                </td>
                <td className='table-right-border' rowSpan={2}>稅額</td>
                <td rowSpan={2} className="table-left-border"><input type="number" className='textright' defaultValue={resData.taxNumber} onChange={(e) => handleInput(e)} id="checktax"></input></td>
            </tr>

            <tr></tr>

            <tr className='table-inside'>
                <td className='table-right-border' colSpan={4}>總計</td>
                <td className='border'><input type="number" className='textright' defaultValue={resData.totalAddTax} onChange={(e) => handleInput(e)} id="checktotalall"></input></td>
            </tr>

            <tr className='table-inside'>
                <td className='table-right-border' colSpan={3}>新台幣大寫</td>
                <td className='table-left-border' colSpan={2}><input type="text" defaultValue={blockletter} onChange={(e) => handleInput(e)} id="checkblockletter"></input></td>
            </tr>
        </table>
        <table>
            <tr>
                <td>上次修改時間：</td>
                <td>{daterevise}</td>
                <td>修改人員：{inspector}</td>
            </tr>

            <tr>
                <td>共{totalpage}張</td>
                <td>第{resData.page + 1}張</td>
            </tr>
        </table>

        <table>
            <tr>
                <td><input type="button" value="上一張" onClick={upj} /></td>
                <td colSpan={3}><input type="button" value="下一張" onClick={downj} /></td>
            </tr>
        </table>
        <br></br>
        <p>統編" 正確 " 請enable下方選項：</p>
        <Form>
            <Form.Field>
                <Checkbox
                    radio
                    label='統編正確，但此統編客戶不存在，要將此客戶建檔'
                    name='checkboxRadioGroup'
                    value2='統編正確，但此統編客戶不存在，要將此客戶建檔'
                    checked={value2 === '統編正確，但此統編客戶不存在，要將此客戶建檔'}
                    onChange={(e, data2) => setValue2(data2.value2)}
                />
            </Form.Field>
            <Form.Field>
                <Checkbox
                    radio
                    label='不要建檔'
                    name='checkboxRadioGroup'
                    value2='不要建檔'
                    checked={value2 === '不要建檔'}
                    onChange={(e, data2) => setValue2(data2.value2)}
                />
            </Form.Field>
        </Form>
        <br></br>
        <table>
            <tr>
                <td><input type="button" value="放棄修改" onClick={giveupchange} /></td>
                <td className='table-right' colSpan={3}><input type="button" value="儲存修改" onClick={Checkdata} /></td>
            </tr>
        </table>
        <p></p>
        <Link to="/Search"><Button>回查詢頁</Button></Link>

    </div>
}

export default OutAndReviseTable