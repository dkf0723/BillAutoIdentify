import {OutAndReviseTable} from "./OutAndRevise-Table";

global.pages = 0;
global.setnew = 0;
global.numlength = 0;
global.detailList = 0;
//OutAndReviseTable.s
export function setup(){
    const invoicen = "http://127.0.0.1:8080/bill-auto-identify/bill/check";//Account info link
    var page = global.pages;
    var s = {page};
    alert("第幾"+page)
    fetch( invoicen,{
        method:"post",//選擇POST發送
        headers: {
            'Accept': 'application/json',
            'Access-Control-Allow-Origin': '*' ,
            'Content-Type': 'application/json',//轉換json檔
        },
        body: JSON.stringify(s)
                   
        })
        .then(res => {
            console.log(res)
            if (!res.ok) {
                throw new Error("HTTP error " + res.status);
            }
            return res.json();
        })
        .then(info => {
            console.log(info);
            var address = info.address//買受人地址
            var invoicenumber=info.billNumber;//發票號碼
            var invoicetype=info["billType"];//發票二三聯
            var buyer = info["buyer"];//買受人
            var blockletter  = info["chineseTotalAddTax"];//新台幣大寫
            var date = info["dateTime"]
            var datetime=date[0]+"年 "+date[1]+"月 "+date[2]+"日";
    
            var daterevise = info["includeDateTime"].substr(0, 4)+"年 "+
            info["includeDateTime"].substr(5, 2)+
            "月 "+info["includeDateTime"].substr(8, 2)+"日 "+
            info["includeDateTime"].substr(-10, 8);//日期
    
            var includeSource = info["includeSource"];
            var modifyUserId = info["modifyUserId"];
            var picture = info["picture"];
            var number = info["taxIdNumber"];//統一編號
            var tax = info["taxNumber"];//稅額
            var value1 = info["taxType"];//營業稅核取方塊
            var totalmini = info["total"];//合計
            var totalall = info["totalAddTax"];//總計
            var daterange = info["yearMonth"];//發票期間
            global.numlength = info["billDetailList"].length;//目前頁數
            global.detailList = JSON.stringify(["billDetailList"])//發票詳細
            alert(global.numlength);
            
            global.setnew = [address,invoicenumber,invoicetype,buyer,blockletter,date,datetime,
                daterevise,includeSource,modifyUserId,picture,number,tax,value1,totalmini,totalall,daterange]
            //alert(setnew)
            //global.setnew=setnew;
            alert(global.setnew)
        })
        .catch(e => {
            alert(e);
        })//^失敗動作*/
    
       
        /*fetch(invoicen,{
        method:"GET",
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
    .then(info => {
        console.log(info);
        OutAndReviseTable.setAddress(info.address);//買受人地址
        OutAndReviseTable.setInvoicenumber(info.billNumber);//發票號碼
        OutAndReviseTable.setInvoicetype(info["billType"]);//發票二三聯
        OutAndReviseTable.setBuyer(info["buyer"]);//買受人
        OutAndReviseTable.setBlockletter(info["chineseTotalAddTax"]);//新台幣大寫
        var date = info["dateTime"]
        OutAndReviseTable.setDatetime(date[0]+"年 "+date[1]+"月 "+date[2]+"日");

        OutAndReviseTable.setDaterevise(info["includeDateTime"].substr(0, 4)+"年 "+
        info["includeDateTime"].substr(5, 2)+
        "月 "+info["includeDateTime"].substr(8, 2)+"日 "+
        info["includeDateTime"].substr(-10, 8));//日期

        //info["includeSource"]
        //info["modifyUserId"]
        //info["picture"]
        OutAndReviseTable.setNumber(info["taxIdNumber"])//統一編號
        OutAndReviseTable.setTax(info["taxNumber"])//稅額
        OutAndReviseTable.setValue1(info["taxType"])//營業稅核取方塊
        OutAndReviseTable.setTotalmini(info["total"])//合計
        OutAndReviseTable.setTotalall(info["totalAddTax"])//總計
        OutAndReviseTable.setDaterange(info["yearMonth"])//發票期間

    })
    .catch(e => {
        alert(e);
    })//^失敗動作*/
}