function sendPostRequest(e, link, dataToSend, toInsertHtml) {
    $.ajax({
        type: "POST",
        url: link,
        data: dataToSend,
        success: function (result) {
            document.getElementById(toInsertHtml).innerHTML = result;
        }
    })
}