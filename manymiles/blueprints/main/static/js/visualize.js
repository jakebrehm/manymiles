async function fetchData(endpoint) {
    // Make a GET request and get the JSON from the response body
    try {
        const response = await fetch(endpoint);
        // Check to see if there were any issues with the response
        if (!response.ok) {
            throw new Error("Could not fetch data.")
        }
        const data = await response.json();
        return data;
    // Throw any errors that occur
    } catch(error) {
        console.error(error);
    }
}

function cssVariable(variable) {
    // Get the computed style of the document body
    var style = getComputedStyle(document.body);
    // Return the desired variable
    return style.getPropertyValue(variable);
}

function createRecordTimeline(canvasId) {
    // Define the endpoint that data will be retrieved from
    const endpoint = "/data/record_timeline";
    // Get a handle to the canvas that will be used for the visualization
    const canvas = document.getElementById(canvasId);
    // Asynchronously end a GET reqest to fetch the data
    var response = fetchData(endpoint);
    // Create the visualization
    response.then(function(data) {
        // If there aren't enough values, don't create the visualization
        if (!data["valid"]) {
            return
        }
        
        var ctx = canvas.getContext("2d");
        var lineChart = new Chart(ctx, {
            type: "line",
            data: {
                labels: data["labels"],
                datasets: [
                    {
                        label: "Mileage",
                        data: data["values"],
                        fill: false,
                        borderColor: cssVariable("--primary"),
                        lineTension: 0.1
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: "Mileage over time",
                        color: cssVariable("--contrast"),
                        font: {
                            size: 20,
                        },
                        align: "start",
                    }
                },
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: "Date",
                            color: cssVariable("--contrast"),
                            font: {
                                size: 14,
                            },
                        },
                    },
                    y: {
                        title: {
                            display: true,
                            text: "Mileage",
                            color: cssVariable("--contrast"),
                            font: {
                                size: 14,
                            },
                        },
                    },
                },
            }
        });
    })
}

// Create the visualization
createRecordTimeline(canvasId="line-chart")