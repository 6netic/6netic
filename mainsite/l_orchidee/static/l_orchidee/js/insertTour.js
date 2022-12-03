function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

let formTour = document.getElementById("formTour");

formTour.addEventListener("submit", function(e) {
	e.preventDefault();
	document.getElementById("confirmInsert").textContent="";
	sendBtn.style.display = 'none';
	spinnerBtn.style.display = 'block';

	const request = new Request("check_variables", { headers: { 'X-CSRFToken': csrftoken }});
    let formData = new FormData();
    let laDate = date_tour.value;
    let tour = document.getElementById("tour_name").textContent;
    let nurse = document.getElementById("nurse").value;

    formData.append("date_tour", laDate);
    formData.append("tour_name", tour);
    formData.append("nurse", nurse);
    formData.append("pdf_file", pdf_file.files[0]);
	/* Ajax function */
	fetch(request, { method: "POST", mode: "same-origin", body: formData })
	.then(function(response) {
        let displayResponse = function (customColor) {
            response.json().then(function(data) {
                document.getElementById("sendBtn").style.display = 'block';
                const spinnerBtn = document.getElementById("spinnerBtn");
                spinnerBtn.style.display = 'none';
                const confirmInsert = document.getElementById("confirmInsert");
                confirmInsert.style.color = customColor;
                confirmInsert.textContent = data.message;
            });
	    }
        if (response.status == 200) {
            displayResponse ("green");
            document.getElementById("first_tour").style.display = 'none';
            document.getElementById("second_tour").style.display = 'block';
        } else if (response.status == 220) { displayResponse ("red");
        } else if (response.status == 221) { displayResponse ("red");
        } else if (response.status == 222) { displayResponse ("red");
        }
    })
    .catch(function(error) {
        console.log("Il y a eu un problème avec l'opération fetch.");
    });
});
