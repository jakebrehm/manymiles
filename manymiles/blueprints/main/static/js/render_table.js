function dataframeToHTML(json_string) {
    const dataframe = JSON.parse(json_string);

    dataframe["columns"].forEach((element) => {
        console.log(element)
    });

    let html = "";
    
    html += `<table role="grid">`;
    html += `<thead>`;
    dataframe["columns"].forEach((column) => {
        html += `<th>${column}</th>`;
    });
    html += `</thead>`;
    html += `<tbody>`;
    dataframe["data"].forEach((row) => {
            html += `<tr>`;
            row.forEach((item) => {
                html += `<td>${item}</td>`;
            });
            html += `</tr>`;
    });
    html += `</tbody>`;
    html += `</table>`;

    console.log(html)

    return html;
}

function renderRecordTable() {
    const button = document.getElementById("table-button");
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (xhttp.readyState === XMLHttpRequest.DONE) {
            document.getElementById("table").innerHTML = dataframeToHTML(xhttp.responseText);
            button.setAttribute("aria-busy", "false");
        }
    }
    xhttp.open("POST", "/_get_records", true);
    button.setAttribute("aria-busy", true);
    xhttp.send();
}