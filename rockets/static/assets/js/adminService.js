
// optimize: 서비스 조회 기능
const tbody = document.getElementById('serviceTbody');

// 만약 svcList가 비어있다면 메시지를 화면에 추가
if (svcList.length === 0) {
    const tr_blank = document.createElement('tr');
    const td_blank = document.createElement('td');
    td_blank.colSpan = 5;  // 테이블 열 전체를 차지하도록 설정
    td_blank.innerText = "운영하는 서비스가 없습니다.";
    td_blank.classList.add("table-blank-class");
    td_blank.style.pointerEvents = "none";
    tr_blank.appendChild(td_blank);
    tbody.appendChild(tr_blank);

} else {
    for(let i=0; i<svcList.length; i++){
    
        const tr = document.createElement('tr');
        tr.className = "tr-row";
        tr.id = "serviceRow";
        tr.style.textAlign = "center";
        tr.style.verticalAlign = "middle";
        tr.style.cursor = "pointer";
        tr.style.pointerEvents = "hover";
    
        
        const serviceId = document.createElement('input');
        serviceId.type = "hidden";
        serviceId.className = "serviceListId-row";
        serviceId.value = svcList[i].service_no;
    
    
    
        // optimize: 서비스 상태 상세 조회 (클릭할때)
        tr.addEventListener('click', () => {
    
            const serviceListId = document.getElementsByClassName('serviceListId-row');
            console.log(serviceListId[i].value);
    
            fetch('/rocketadmin/service/info/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({serviceListId : serviceListId[i].value})
        
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('네트워크 응답이 올바르지 않습니다.');
                }
                return response.json();
            })
            .then( data => {
                console.log(data)
                const serviceinfo = JSON.parse(data.serviceInfo);
                // console.log(serviceinfo.service_name);
                serviceInfo(serviceinfo);
            })
            .catch(error => {
                console.error('serviceInfo 요청 중 오류 발생:', error);
            });
        });
    
    
        const td1 = document.createElement('td');
        td1.innerText = i+1;
        td1.style.width = "100px";
    
        const td2 = document.createElement('td');
        td2.innerText = svcList[i].service_name;  
        
        const td3 = document.createElement('td');
        td3.innerText = svcList[i].user_name;  
        td3.style.width = "200px";
    
    
        // todo: 서비스 생성 부분 나중에 처리하기
        const td4 = document.createElement('td');
        td4.innerText = svcList[i].create_date;  
        td4.style.width = "250px";
        
        const td5 = document.createElement('td');
        td5.innerText = 'serviceStatus'; 
        td5.style.width = "200px";

        const td6 = document.createElement('td');
        const delbtn = document.createElement('button');
        delbtn.type = "button";
        delbtn.className = "btn btn-outline-danger delete-btn";
        delbtn.innerText = "삭제";
        td6.append(delbtn);
        
    
        tr.append(td1, td2, td3, td4, td5, td6, serviceId);
        tbody.append(tr);
    
    }
}


const infoTbody = document.getElementById('infoTbody');


/** 
 * 서비스 상세 정보 출력 함수
 * @param {serviceInfo} fetch로 불러온 서비스 상세 정보
*/
const serviceInfo = (serviceInfo) => {

    document.getElementById("infoTbody").innerText = "";

    // 서비스 이름
    const tr1 = document.createElement('tr');
    tr1.scope = "col";
    
    const td11 = document.createElement('td');
    td11.innerText = "서비스명";
    td11.classList.add("serviceInfoThead");
    
    const td12 = document.createElement('td');
    td12.innerText = serviceInfo.service_name;

    tr1.append(td11, td12);


    // 서비스 상태
    const tr2 = document.createElement('tr');
    tr2.scope = "col";

    const td21 = document.createElement('td');
    td21.innerText = "상태";
    td21.classList.add("serviceInfoThead");

    const td22 = document.createElement('td');
    td22.innerText = "Running";  //fixme: 상태 정보 추후 수정하기

    tr2.append(td21, td22);


    // 서비스 생성 날짜
    const tr3 = document.createElement('tr');
    tr3.scope = "col";

    const td31 = document.createElement('td');
    td31.innerText = "생성일"
    td31.classList.add("serviceInfoThead");

    const td32 = document.createElement('td');
    td32.innerText = serviceInfo.create_date;

    tr3.append(td31, td32);


    // 지역
    const tr4 = document.createElement('tr');
    tr4.scope = "col";

    const td41 = document.createElement('td');
    td41.innerText = "지역 (Region)";
    td41.classList.add("serviceInfoThead");

    const td42 = document.createElement('td');
    td42.innerText = serviceInfo.region_name;

    tr4.append(td41, td42);

    
    // 로드밸런서 주소 or ip주소
    const tr5 = document.createElement('tr');
    tr5.scope = "col";

    const td51 = document.createElement('td');
    td51.innerText = "주소 (LB)";
    td51.classList.add("serviceInfoThead");
    
    const td52 = document.createElement('td');
    // td52.innerText = serviceInfo.load_balancer_address;
    td52.innerText = serviceInfo.load_balancer_name !== undefined ? serviceInfo.load_balancer_name : '';
 

    tr5.append(td51, td52);


    // 프론트엔드 사용여부
    const tr6 = document.createElement('tr');
    tr6.scope = "col";

    const td61 = document.createElement('td');
    td61.innerText = "프론트엔드";
    td61.classList.add("serviceInfoThead");

    const td62 = document.createElement('td');

    if(serviceInfo.frontend_fl == "Y"){
        td62.innerText = "사용";
    } else if(serviceInfo.frontend_fl == "N"){
        td62.innerText = "미사용";
    }

    tr6.append(td61, td62);

    // 백엔드 언어
    const tr7 = document.createElement('tr');
    tr7.scope = "col";

    const td71 = document.createElement('td');
    td71.innerText = "백엔드";
    td71.classList.add("serviceInfoThead");

    const td72 = document.createElement('td');
    td72.innerText = serviceInfo.backend_name;

    tr7.append(td71, td72);

    // ecr_uri
    const tr8 = document.createElement('tr');
    tr8.scope = "col";

    const td81 = document.createElement('td');
    td81.innerText = "ECR URI";
    td81.classList.add("serviceInfoThead");

    const td82 = document.createElement('td');
    // td82.innerText = serviceInfo.ecr_uri;
    td82.innerText = serviceInfo.ecr_uri !== undefined ? serviceInfo.ecr_uri : '';

    tr8.append(td81, td82);


    // s3_arn
    const tr9 = document.createElement('tr');
    tr9.scope = "col";

    const td91 = document.createElement('td');
    td91.innerText = "S3 ARN";
    td91.classList.add("serviceInfoThead");
    td82.innerText = serviceInfo.s3_arn !== undefined ? serviceInfo.s3_arn  : '';

    const td92 = document.createElement('td');
    td92.innerText = serviceInfo.s3_arn;

    tr9.append(td91, td92);


    // 전체 합치기
    infoTbody.append(tr1, tr2, tr3, tr4, tr5, tr6, tr7, tr8, tr9);
}


