function getCookie(name) {
    function escape(s) { return s.replace(/([.*+?\^$(){}|\[\]\/\\])/g, '\\$1'); }
    var match = document.cookie.match(RegExp('(?:^|;\\s*)' + escape(name) + '=([^;]*)'));
    return match ? match[1] : null;
}


function deleteRecord(id) {

    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (xhttp.readyState == 4 && xhttp.status == 200) {
            var res = JSON.parse(xhttp.responseText);

            if(res['status'] == 1) {
                var emt = document.querySelector('#record-' + id);
                emt.remove();
            }
        }
    };
    
    xhttp.open("POST", "/manage/delete/", true);
    xhttp.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
    var data = {
        "id": id, 
    }
    xhttp.send(JSON.stringify(data));
}


function addRecord() {

    var inputEmt = document.querySelector('.add-item-container input');
    if(inputEmt.value.length == 0) {
        alert('請輸入語錄~');
        return;
    }

    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (xhttp.readyState == 4 && xhttp.status == 200) {
            var res = JSON.parse(xhttp.responseText);

            if(res['status'] == 1) {
                var itemContainer = document.querySelector('.item-container');

                var newItem = document.createElement('div');
                newItem.classList = 'item';
                newItem.id = 'record-' + res['id'];

                var newSpan1 = document.createElement('span');
                newSpan1.classList = 'item-text';
                newSpan1.innerHTML = inputEmt.value;

                var newSpan2 = document.createElement('span');
                newSpan2.classList = 'item-btn';
                newSpan2.innerHTML = '刪除';
                newSpan2.setAttribute('onclick', `deleteRecord(${res['id']})`);
                

                newItem.appendChild(newSpan1);
                newItem.appendChild(newSpan2);
                itemContainer.appendChild(newItem);
            }
        }
    };
    
    xhttp.open("POST", "/manage/add/", true);
    xhttp.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
    var data = {
        "text": inputEmt.value, 
    }
    xhttp.send(JSON.stringify(data));
}