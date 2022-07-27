$(document).ready(function(){
    const listViewButton = document.querySelector('.list-view-button');
    const gridViewButton = document.querySelector('.grid-view-button');
    const list = document.querySelector('.list-of-cards');

    listViewButton.onclick = function () {

        if(!$(list).hasClass('type-list')){
            $('.view-btn-group .btn').removeClass('active');
            list.classList.remove('type-grid');
            list.classList.add('type-list');
            $(this).addClass('active');
        }
    }

    gridViewButton.onclick = function () {
        if(!$(list).hasClass('type-grid')){
            $('.view-btn-group .btn').removeClass('active');
            list.classList.remove('type-list');
            list.classList.add('type-grid');
            $(this).addClass('active');
        }

    }
//ends
});
