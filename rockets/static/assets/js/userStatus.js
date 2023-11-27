
console.log("hi");

const tbody = document.getElementById('serviceTbody');

// TODO: db 가져와서 변수 바꾸기
const list = 8;

for(let i=0; i<list; i++){
    const tr = document.createElement('tr');
    tr.className = "tr-row";

    const td1 = document.createElement('td');
    td1.innerText = i+1;

    const td2 = document.createElement('td');
    td2.innerText = "date";  // TODO: 데이터베이스 불러오기

    const td3 = document.createElement('td');
    td3.innerText = 'serviceName'; // TODO: 데이터베이스 불러오기

    const td4 = document.createElement('td');
    td4.innerText = 'serviceStatus'; // TODO: 데이터베이스 불러오기

    const td5 = document.createElement('td');
    const delbtn = document.createElement('button');
    delbtn.type = "button";
    delbtn.className = "btn btn-outline-danger delete-btn";
    delbtn.innerText = "삭제";
    td5.append(delbtn);
    

    tr.append(td1, td2, td3, td4, td5);
    tbody.append(tr);
}
