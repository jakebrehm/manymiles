function dataframeToHTML(json_string) {
    const dataframe = JSON.parse(json_string);

    let html = "";
    
    html += `<table role="grid">`;
    html += `<thead>`;
    dataframe["columns"].forEach((column) => {
        html += `<th>${column}</th>`;
    });
    html += `<th></th>`;
    // for (let [index, column] of dataframe["columns"].entries()) {
    //     console.log(index);
    //     if ([0, 1, 2, 3].includes(index)) {
    //         html += `<th style="width: 15%">${column}</th>`;
    //     } else {
    //         html += `<th>${column}</th>`;
    //     }
    // }
    html += `</thead>`;
    html += `<tbody>`;
    dataframe["data"].forEach((row) => {
            html += `<tr>`;
            row.forEach((item) => {
                if (row)
                html += `<td>${item}</td>`;
            });
            html += `<td>`;
            html += `<a href="/delete_record?record=${row[0]}" role="button"><i class="fa fa-trash-o fa-fw"></i></a>`;
            html += `<a href="/update?record=${row[0]}" role="button"><i class="fa fa-edit fa-fw"></i></a>`;
            html += `</td>`;
            html += `</tr>`;
    });
    html += `</tbody>`;
    html += `</table>`;

    return html;
}

// function()

function renderRecordTable() {
    const button = document.getElementById("table-button");
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (xhttp.readyState === XMLHttpRequest.DONE) {
            document.getElementById("table").innerHTML = dataframeToHTML(
                xhttp.responseText
            );
            button.setAttribute("aria-busy", "false");
        }
    }
    xhttp.open("POST", "/_get_records", true);
    button.setAttribute("aria-busy", true);
    xhttp.send();
}