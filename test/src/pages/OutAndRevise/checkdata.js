import {OutAndReviseTable} from "./OutAndRevise-Table";
global.data = "";
global.taxbox="";
export function Checkdata(){
    const checkok = "成功";//初始設定
    /*var checkinvoicenumber = document.getElementById("checkinvoicenumber").value;//修改確認發票號碼
    var checkinvoicetype = document.getElementById("checkinvoicetype").value;//修改確認發票二三聯
    var checkdaterange = document.getElementById("checkdaterange").value;//修改確認發票期間
    var checknumber = document.getElementById("checknumber").value;//修改確認統一編號
    var checkdatetime = document.getElementById("checkdatetime").value;//修改確認日期
    var checkbuyer = document.getElementById("checkbuyer").value;//修改確認買受人
    var checkaddress = document.getElementById("checkaddress").value;//修改確認地址
    var checktotalmini = document.getElementById("checktotalmini").value;//修改確認合計
    var checktax = document.getElementById("checktax").value;//修改確認稅額
    var checktotalall = document.getElementById("checktotalall").value;//修改確認總計
    var checkblockletter = document.getElementById("checkblockletter").value;//修改確認新台幣大寫
    var checkr1c1 = document.getElementById("r1c1").value;//修改確認
    var checkr1c2 = document.getElementById("r1c2").value;
    var checkr1c3 = document.getElementById("r1c3").value;
    var checkr1c4 = document.getElementById("r1c4").value;
    var checkr1c5 = document.getElementById("r1c5").value;
    var checkr2c1 = document.getElementById("r2c1").value;//修改確認
    var checkr2c2 = document.getElementById("r2c2").value;
    var checkr2c3 = document.getElementById("r2c3").value;
    var checkr2c4 = document.getElementById("r2c4").value;
    var checkr2c5 = document.getElementById("r2c5").value;
    var checkr3c1 = document.getElementById("r3c1").value;//修改確認
    var checkr3c2 = document.getElementById("r3c2").value;
    var checkr3c3 = document.getElementById("r3c3").value;
    var checkr3c4 = document.getElementById("r3c4").value;
    var checkr3c5 = document.getElementById("r3c5").value;
    var checkr4c1 = document.getElementById("r4c1").value;//修改確認
    var checkr4c2 = document.getElementById("r4c2").value;
    var checkr4c3 = document.getElementById("r4c3").value;
    var checkr4c4 = document.getElementById("r4c4").value;
    var checkr4c5 = document.getElementById("r4c5").value;
*/
//統一編號檢測
var errorlist="錯誤內容："
//const numbercheck = global.data.billNumber; 
const numbercheck = document.getElementById("checknumber").value;
const one = parseInt(numbercheck.substring(0,1),10); //8碼中第1位，字串轉10進位數字
const two = parseInt(numbercheck.substring(1,2),10); //8碼中第2位，字串轉10進位數字
const three = parseInt(numbercheck.substring(2,3),10); //8碼中第3位，字串轉10進位數字
const four = parseInt(numbercheck.substring(3,4),10); //8碼中第4位，字串轉10進位數字
const five = parseInt(numbercheck.substring(4,5),10); //8碼中第5位，字串轉10進位數字
const six = parseInt(numbercheck.substring(5,6),10); //8碼中第6位，字串轉10進位數字
const seven = parseInt(numbercheck.substring(6,7),10); //8碼中第7位，字串轉10進位數字
const eight = parseInt(numbercheck.substring(7,8),10); //8碼中第8位，字串轉10進位數字

const checknum = [1,2,1,2,1,2,4,1];//財政部統編檢核邏輯參數

//----取得第一、二位的值
const onenum = String(one * checknum[0]);//第一位計算乘績轉字串
const a = parseInt(onenum.substring(0,1),10);//取第一位轉數字
const a1 = parseInt(onenum.substring(1,2),10);//取第二位轉數字
if(String(a1) === 'NaN'){//檢查第二位數值是否錯誤
    var a2 = 0;//初始化第二位數值
}
else{
    a2 = a1;
}

const twonum = String(two * checknum[1]);//第二位計算乘績轉字串
const b = parseInt(twonum.substring(0,1),10);//取第一位轉數字
const b1 = parseInt(twonum.substring(1,2),10);//取第二位轉數字
if(String(b1) === 'NaN'){//檢查第二位數值是否錯誤
    var b2 = 0;//初始化第二位數值
}
else{
    b2 = b1;
}

const threenum = String(three * checknum[2]);//第三位計算乘績轉字串
const c = parseInt(threenum.substring(0,1),10);//取第一位轉數字
const c1 = parseInt(threenum.substring(1,2),10);//取第二位轉數字
if(String(c1) === 'NaN'){//檢查第二位數值是否錯誤
    var c2 = 0;//初始化第二位數值
}
else{
    c2 = c1;
}

const fournum = String(four * checknum[3]);//第四位計算乘績轉字串
const d = parseInt(fournum.substring(0,1),10);//取第一位轉數字
const d1 = parseInt(fournum.substring(1,2),10);//取第二位轉數字
if(String(d1) === 'NaN'){//檢查第二位數值是否錯誤
    var d2 = 0;//初始化第二位數值
}
else{
    d2 = d1;
}

const fivenum = String(five * checknum[4]);//第五位計算乘績轉字串
const e = parseInt(fivenum.substring(0,1),10);//取第一位轉數字
const e1 = parseInt(fivenum.substring(1,2),10);//取第二位轉數字
if(String(e1) === 'NaN'){//檢查第二位數值是否錯誤
    var e2 = 0;//初始化第二位數值
}
else{
    e2 = e1;
}

const sixnum = String(six * checknum[5]);//第六位計算乘績轉字串
const f = parseInt(sixnum.substring(0,1),10);//取第一位轉數字
const f1 = parseInt(sixnum.substring(1,2),10);//取第二位轉數字
if(String(f1) === 'NaN'){//檢查第二位數值是否錯誤
    var f2 = 0;//初始化第二位數值
}
else{
    f2 = f1;
}

const sevennum = String(seven * checknum[6]);//第七位計算乘績轉字串
const g = parseInt(sevennum.substring(0,1),10);//取第一位轉數字
const g1 = parseInt(sevennum.substring(1,2),10);//取第二位轉數字
if(String(g1) === 'NaN'){//檢查第二位數值是否錯誤
    var g2 = 0;//初始化第二位數值
}
else{
    g2 = g1;
}

const eightnum = String(eight * checknum[7]);//第八位計算乘績轉字串
const h = parseInt(eightnum.substring(0,1),10);//取第一位轉數字
const h1 = parseInt(eightnum.substring(1,2),10);//取第二位轉數字
if(String(h1) === 'NaN'){//檢查第二位數值是否錯誤
    var h2 = 0;//初始化第二位數值
}
else{
    h2 = h1;
}
//---- 
//第一位a b c d e f g h；第二位a2 b2 c2 d2 e2 f2 g2 h2

if(seven !== 7){//第七碼不等於7
    const sum = a+a2+b+b2+c+c2+d+d2+e+e2+f+f2+g+g2+h+h2;
    const remainder5 =sum % 5;
    const remainder10 =sum % 10;
    if(remainder5==0 || remainder10==0){
        document.getElementById("checknumber").style.color="";//文字原色
    }
    else{
        errorlist+="/錯誤統編";
        document.getElementById("checknumber").style.color="red";//錯誤文字變紅色
    }
}
else{
    //sum、sum1 其一可被10或5整除
    const sum = a+a2+b+b2+c+c2+d+d2+e+e2+f+f2+1+h+h2;//規則第7位和=10，取十位數
    const sum1 = a+a2+b+b2+c+c2+d+d2+e+e2+f+f2+0+h+h2;//規則第7位和=10，取個位數
    const remainder5 =sum % 5;
    const remainder51 =sum1 % 5;
    const remainder10 =sum % 10;
    const remainder101 =sum1 % 10;
    if(remainder5==0 || remainder10==0 || remainder51==0 || remainder101==0){
        document.getElementById("checknumber").style.color="";//文字原色
        //setR1C1(sum1);//更換input值
    }
    else{
        errorlist+="/錯誤統編";
        document.getElementById("checknumber").style.color="red";//錯誤文字變紅色
    }
}
//-----統一編號檢測 結束
/*
//金額檢核=單價*數量 ； 零稅率/免稅之稅額=空白 or 0
document.getElementById("r2c1").style.color="";//文字原色
document.getElementById("r3c1").style.color="";//文字原色
document.getElementById("r4c1").style.color="";//文字原色
if(parseInt(checkr4c1,10) !== parseInt(checkr2c1,10)*parseInt(checkr3c1)){
    document.getElementById("r2c1").style.color="red";//錯誤文字變紅色
    document.getElementById("r3c1").style.color="red";//錯誤文字變紅色
    document.getElementById("r4c1").style.color="red";//錯誤文字變紅色
    errorlist+="/項次1-金額錯誤";
}

document.getElementById("r2c2").style.color="";//文字原色
document.getElementById("r3c2").style.color="";//文字原色
document.getElementById("r4c2").style.color="";//文字原色
if(parseInt(checkr4c2,10) !== parseInt(checkr2c2,10)*parseInt(checkr3c2)){
    document.getElementById("r2c2").style.color="red";//錯誤文字變紅色
    document.getElementById("r3c2").style.color="red";//錯誤文字變紅色
    document.getElementById("r4c2").style.color="red";//錯誤文字變紅色
    errorlist+="/項次2-金額錯誤";
}

document.getElementById("r2c3").style.color="";//文字原色
document.getElementById("r3c3").style.color="";//文字原色
document.getElementById("r4c3").style.color="";//文字原色
if(parseInt(checkr4c3,10) !== parseInt(checkr2c3,10)*parseInt(checkr3c3)){
    document.getElementById("r2c3").style.color="red";//錯誤文字變紅色
    document.getElementById("r3c3").style.color="red";//錯誤文字變紅色
    document.getElementById("r4c3").style.color="red";//錯誤文字變紅色
    errorlist+="/項次3-金額錯誤";
}

document.getElementById("r2c4").style.color="";//文字原色
document.getElementById("r3c4").style.color="";//文字原色
document.getElementById("r4c4").style.color="";//文字原色
if(parseInt(checkr4c4,10) !== parseInt(checkr2c4,10)*parseInt(checkr3c4)){
    document.getElementById("r2c4").style.color="red";//錯誤文字變紅色
    document.getElementById("r3c4").style.color="red";//錯誤文字變紅色
    document.getElementById("r4c4").style.color="red";//錯誤文字變紅色
    errorlist+="/項次4-金額錯誤";
}

document.getElementById("r2c5").style.color="";//文字原色
document.getElementById("r3c5").style.color="";//文字原色
document.getElementById("r4c5").style.color="";//文字原色
if(parseInt(checkr4c5,10) !== parseInt(checkr2c5,10)*parseInt(checkr3c5)){
    document.getElementById("r2c5").style.color="red";//錯誤文字變紅色
    document.getElementById("r3c5").style.color="red";//錯誤文字變紅色
    document.getElementById("r4c5").style.color="red";//錯誤文字變紅色
    errorlist+="/項次5-金額錯誤";
}
//金額檢核=單價*數量 ； 零稅率/免稅之稅額=空白 or 0 結束

//合計檢核=sum(1~5項的金額)
document.getElementById("checktotalmini").style.color="";//文字原色
//alert(totalmini+parseInt(r4c1,10)+parseInt(r4c2,10)+parseInt(r4c3,10)+parseInt(r4c4,10)+parseInt(r4c5,10));

if(parseInt(checktotalmini,10) !== parseInt(checkr4c1,10)+parseInt(checkr4c2,10)+parseInt(checkr4c3,10)+parseInt(checkr4c4,10)+parseInt(checkr4c5,10)){
    document.getElementById("r4c1").style.color="orange";//錯誤文字變紅色
    document.getElementById("r4c2").style.color="orange";//錯誤文字變紅色
    document.getElementById("r4c3").style.color="orange";//錯誤文字變紅色
    document.getElementById("r4c4").style.color="orange";//錯誤文字變紅色
    document.getElementById("r4c5").style.color="orange";//錯誤文字變紅色
    document.getElementById("checktotalmini").style.color="red";//錯誤文字變紅色
    errorlist+="/合計錯誤"
}
*/
//合計檢核=sum(1~5項的金額) 結束

//應稅時的稅額=合計*0.05
document.getElementById("checktax").style.color="";//文字原色
if(global.taxbox==="應稅"){
    if(document.getElementById("checktax").value!==""){
        var taxcheck = parseInt(document.getElementById("checktax").value,10);
        if(taxcheck!== parseInt(document.getElementById("checktotalmini").value,10)*0.05){
            //document.getElementById("checktotalmini").style.color="orange";//錯誤文字變紅色
            document.getElementById("checktax").style.color="red";//錯誤文字變紅色
            errorlist+="/稅額錯誤"
        }
    }  
}
else{
    if(document.getElementById("checktax").value!==""){
        if(document.getElementById("checktax").value !=="0"){
            //document.getElementById("checktotalmini").style.color="orange";//錯誤文字變紅色
            document.getElementById("checktax").style.color="red";//錯誤文字變紅色
            errorlist+="/稅額錯誤(零稅率或免稅)"
        }           
    }
}
//應稅時的稅額=合計*0.05 結束  

//總計檢核=合計+稅額
document.getElementById("checktotalall").style.color="";//文字原色
if(document.getElementById("checktax").value===""){
    //OutAndReviseTable.setTax("0");
}
if(parseInt(document.getElementById("checktotalall").value,10)!==(parseInt(document.getElementById("checktotalmini").value,10)+parseInt(document.getElementById("checktax").value,10))){
    //document.getElementById("checktax").style.color="orange";//錯誤文字變紅色
    document.getElementById("checktotalall").style.color="red";//錯誤文字變紅色
    errorlist+="/總計錯誤"
}
/*
//數字轉大寫(未完成)

var transform = parseInt(checktotalall,10);
var checktotalalllength = parseInt(checktotalall.length);
var block = ["零","壹","貳","叁","肆","伍","陸","柒","捌","玖"];
var digitalunit = ["億","仟","佰","拾","萬","仟","佰","拾","元"];
var checktotalallstring = toString(transform);
//alert(checktotalallstring);

//總計檢核=合計+稅額 結束
    
    if((errorlist)==="錯誤內容："){
        alert("所有內容無誤，儲存成功！");
    }
    else{
        alert(errorlist+="，請再次確認！");
    }
//儲存修改檢測，無誤送出 結束
*/
}