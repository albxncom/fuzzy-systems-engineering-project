advancedView = false

function show_results(data) {

    d = JSON.parse(data)

    if(advancedView) {
        $(".cont_results").removeClass("container")
    }
    else {
        $(".cont_results").addClass("container")
    }

    if (d.data.length > 0) {

        html = '<table class="table table-sm table-striped">'
        html += '<thead>'
        html += '<tr>'
        html += '<th scope="col">' + d.columns[0] + '</th>'
        html += '<th scope="col">' + d.columns[1] + '</th>'
        if(advancedView){
            for (var i = 2; i < d.columns.length; i++) {
                html += '<th scope="col">' + d.columns[i] + '</th>'
            }
        }
        html += '</tr>'
        html += '</thead>'
        html += '<tbody>'


        // for each course, display:
        d.data.forEach(course => {
            html += '<tr>'
            html += '<th scope="row">' + course[0] + '</th>'
            html += '<th scope="row">' + (parseFloat(course[1])).toFixed(2) + '</th>'
            
            if(!advancedView){
                html += ''
            }
            else {
                
                for (var i = 2; i < course.length; i++) {
                    html += '<td>' + course[i] + '</td>'
                }
                
            }
            html += '</tr>'

        });

        html += '</tbody>'
        html += '</table>'

        //write results to field
        $(".results").html(html)
    } else {
        console.log("No courses found...")
    }
}

$(function() {

    $("input[name='tracks']").eq(0).prop("checked", true);
    $("input[name='tracks']").eq(1).prop("checked", true);
    $("input[name='tracks']").eq(2).prop("checked", true);
    $("input[name='tracks']").eq(3).prop("checked", true);
    $("input[name='tracks']").eq(4).prop("checked", true);
    $("input[name='preferred_lang']").eq(0).prop("checked", true);
    $("input[name='preferred_lang']").eq(1).prop("checked", true);
    $("input[name='preferred_lang']").eq(2).prop("checked", true);
    $("input[name='exercices_mandatory_ok']").eq(1).prop("checked", true);
    $("input[name='language_lecture']").eq(1).prop("checked", true);
    $("input[name='language_exercises']").eq(2).prop("checked", true);
    $("input[name='understandability']").eq(3).prop("checked", true);
    $("input[name='difficulty']").eq(1).prop("checked", true);
    $("input[name='commitment']").eq(2).prop("checked", true);
    $("input[name='effort']").eq(4).prop("checked", true);

    $("#evaluate").click(function() {
        var tracks = [];
        var exercices_mandatory_ok;
        var preferred_lang = [];
        var language_lecture;
        var language_exercises;
        var understandability;
        var difficulty;
        var commitment;
        var effort;





        //multiple choice
        $("input[name='tracks']:checked").map(i => tracks.push($("input[name='tracks']:checked").eq(i).val()));
        $("input[name='preferred_lang']:checked").map(i => preferred_lang.push($("input[name='preferred_lang']:checked").eq(i).val()));

        exercices_mandatory_ok = $("input[name='exercices_mandatory_ok']:checked").val() / 5;
        language_lecture = $("input[name='language_lecture']:checked").val() / 5;
        language_exercises = $("input[name='language_exercises']:checked").val() / 5;
        understandability = $("input[name='understandability']:checked").val() / 5;
        difficulty = $("input[name='difficulty']:checked").val() / 5;
        commitment = $("input[name='commitment']:checked").val() / 5;
        effort = $("input[name='effort']:checked").val() / 5;


        var params = {
            "tracks": {
                "var": tracks,
                "name": "tracks"
            },
            "exercices_mandatory_ok": {
                "var": Boolean(exercices_mandatory_ok),
                "name": "exercices_mandatory_ok"
            },
            "preferred_lang": {
                "var": preferred_lang,
                "name": "preferred_lang"
            },
            "language_lecture": {
                "var": language_lecture,
                "name": "language_lecture"
            },
            "language_exercises": {
                "var": language_exercises,
                "name": "language_exercises"
            },
            "understandability": {
                "var": understandability,
                "name": "understandability"
            },
            "difficulty": {
                "var": difficulty,
                "name": "difficulty"
            },
            "commitment": {
                "var": commitment,
                "name": "commitment"
            },
            "effort": {
                "var": effort,
                "name": "effort"
            },
            "quality": {
                "var": 1,
                "name": "quality"
            }
        }

        missing = "";
        complete = true;
        for (const [key, value] of Object.entries(params)) {
            if (value.var === undefined || value.var.length == 0) {
                missing = missing + ", " + value.name;
                complete = false;
            }
        }
        if (!complete) {
            missing = missing.substring(2)

            alert("Missing values: " + missing);
        } else {
            var xhttp = new XMLHttpRequest();
            xhttp.onreadystatechange = function() {
                if (xhttp.readyState === 4) {
                    show_results(xhttp.response);
                }
            }
            xhttp.open("POST", "http://127.0.0.1:8080/fuzzy", true);
            xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
            xhttp.send(JSON.stringify(params));

        }




        return false;
    })

    $(".advancedView").click(function(){
        if(advancedView){
            advancedView = false
            $(this).html("Advanced View")
        } else {
            advancedView = true
            $(this).html("Simple View")
        }
        
        return false;
    })
});