var event;
var attendQuery;

$(document).ready(function () {
    //docReady();
});

function clickedop(numero)
{
    $.ajax({url:'/canal/' + numero});
}


