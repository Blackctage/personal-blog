const burger = document.getElementById('SidebarToggle');
const sidebar = document.getElementById('slidebar');
const page = document.getElementById('page');
const body = document.body;

burger.addEventListener('click', event => {
    if( body.classList.contains('show-slider') ) {
        closeSidebar();
    } else {
        showSidebar();
    }
});

function showSidebar() {
    let mask = document.createElement('div');
    mask.classList.add('page-mask');
    mask.addEventListener('click', closeSidebar);
    page.appendChild(mask);

    body.classList.add('show-slider');
}

function closeSidebar() {
    body.classList.remove('show-slider');
    document.querySelector('.page-mask').remove();
}