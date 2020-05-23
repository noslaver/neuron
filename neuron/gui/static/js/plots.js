$("#type-select").on("change",() => {
    $.ajax({
        url: "/result",
        type: "GET",
        contentType: "application/json;charset=UTF-8",
        data: {
            "selected": document.getElementById("type-select").value
        },
        dataType:"json",
        success: (data) => {
            Plotly.newPlot("bargraph", data );
        }
    });
})
