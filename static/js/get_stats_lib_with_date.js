function isValidDate(dateString) {
    let regEx = /^\d{4}-\d{2}-\d{2}$/;
    if(!dateString.match(regEx)) return false;
    let d = new Date(dateString);
    let dNum = d.getTime();
    if(!dNum && dNum !== 0) return false;
    return d.toISOString().slice(0,10) === dateString;
}

function getStatsByDate(e, link) {
    let since_date_element = document.getElementById('id-since-date')
    let to_date_element = document.getElementById('id-to-date')

    if (!isValidDate(since_date_element.value) || !isValidDate(to_date_element.value)) {
        return
    }

    $.ajax({
        type: "POST",
        url: link,
        data: {
            csrfmiddlewaretoken: csr_token,
            since_date: since_date_element.value,
            to_date: to_date_element.value,
        },
        success: function (result) {
            document.getElementById('table-stats').innerHTML = result;
        }
    })
}