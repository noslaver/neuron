$("#type-select").on("change",() => {
    url = window.location.href;
    ty = document.getElementById("type-select").value;
    $('#carousel').attr('hidden', true);
    $.ajax({
        url: `${url}/result`,
        type: "GET",
        contentType: "application/json;charset=UTF-8",
        data: {
            "selected": ty
        },
        dataType:"json",
        success: (data) => {
            if (ty == "pose" || ty == "feelings")
            {
                Plotly.newPlot("graphs", data);
            }
            else
            {
                Plotly.purge("graphs");

                $('#carousel').attr('hidden', false);

                $('#carousel > div').empty();

                let first = true;
                $.each(data, (_, elem) => {
                    if (first)
                    {
                        $('#carousel > div').append($('<div class="carousel-item item active"><img class="d-block img-fluid" src='  + elem.data_url + '></div>'));
                        first = false;
                    }
                    else
                    {
                        $('#carousel > div').append($('<div class="carousel-item item"><img class="d-block img-fluid" src='  + elem.data_url + '></div>'));
                    }
                 });

                $('.carousel-control-prev').click(() => {
                    $('#carousel').carousel('prev');
                });

                $('.carousel-control-next').click(() => {
                    $('#carousel').carousel('next');
                });

                $('#carousel').carousel({
                    interval: 500,
                    pause: true
                });
            }
        }
    });
})
