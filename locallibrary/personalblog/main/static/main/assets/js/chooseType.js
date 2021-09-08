const chooseTypeBtn = document.querySelectorAll('.search-choose-type-block');
var myURL = window.location.href;

if(myURL.includes('search/&type=post?q=')){
    sessionStorage.setItem('request_type', 'choose-type-Post');
} else if (myURL.includes('search/&type=work?q=')) {
    sessionStorage.setItem('request_type', 'choose-type-Work');
} else if (myURL.includes('search/&type=user?q=')) {
    sessionStorage.setItem('request_type', 'choose-type-User');
}


var test = document.getElementById(sessionStorage.getItem('request_type'))
test.classList.add('chosen-type')
