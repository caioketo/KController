var event;
var attendQuery;

$(document).ready(function () {
    //docReady();
});

function clickedVol(vol)
{
    $.ajax({url:'/volume/' + vol});
}

function clickedop(numero)
{
    $.ajax({url:'/canal/' + numero});
}

function selectedMusic(musicId)
{
    $.ajax({url:'../playmusic/' + musicId});
    alert('Aumenta o Som');
}

function selectedPlaylist(plId)
{
    $.ajax({url:'../playlist/' + plId});
    alert('Aumenta o Som');
}
