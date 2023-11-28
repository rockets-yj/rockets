
console.log("hi");

const tbody = document.getElementById('tbody');

// TODO: db 가져와서 변수 바꾸기
const list = 8;

for(let i=0; i<list; i++){
    console.log("hihi");
    const tr = document.createElement('tr');
    tr.className = "tr-row";

    const td1 = document.createElement('td');
    td1.innerText = i+1;

    const td2 = document.createElement('td');
    td2.innerText = "date";  // TODO: 데이터베이스 불러오기

    const td3 = document.createElement('td');
    td3.innerText = 'username'; // TODO: 데이터베이스 불러오기

    const td4 = document.createElement('td');
    td4.innerText = 'projectName'; // TODO: 데이터베이스 불러오기

    const td5 = document.createElement('td');
    td5.innerText = 'status';

    tr.append(td1, td2, td3, td4, td5);
    tbody.append(tr);
}
