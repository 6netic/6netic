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
var formular = document.getElementById("myForm");
formular.addEventListener("submit", function(e) {
	e.preventDefault();
	let request = new Request("ten_meters", { headers: { 'X-CSRFToken': csrftoken }});
	document.getElementById("message").innerHTML = "";
	const p = document.createElement("p");
	let messResp = document.getElementById("message");
	let paragraph = messResp.appendChild(p);
	const file = document.getElementById("srcfile");
	const formData = new FormData(formular);
	formData.append("srcfile", file.files[0]);

	/* Ajax function */
	fetch(request, { method: "POST", mode: "same-origin", body: formData })
	.then(function(response) {
			if(response.status == 417) {
				response.json().then(function(data) {
					paragraph.innerHTML = data.mess;
				});
			}
			else if(response.status == 415) {
				response.json().then(function(data) {
					paragraph.innerHTML += data.mess;
				})
			}
			else if(response.status == 413) {
				response.json().then(function(data) {
					paragraph.innerHTML += data.mess;
				})
			}
			else {
				response.json().then(function(data) {
					document.getElementById("formBlock").innerHTML = "";
					var output = document.getElementById("picture");
					var image = document.createElement("img");
					image.src = "/static/ciblerie/out/temp.jpg";
					output.appendChild(image);
				})
			}
	})
});


