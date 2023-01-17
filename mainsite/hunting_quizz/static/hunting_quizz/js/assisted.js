
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

var form = document.querySelector("form");
form.addEventListener("submit", function(e) {
  var status = document.getElementById("status");// Pour afficher la réponse
  var verify = document.getElementById("verify");
  let options = form.elements.options.value;
  if (options === "") {
    e.preventDefault();
    status.textContent = "Vous devez sélectionner une proposition valide";
  }
  else {
    e.preventDefault();
    let question_id = form.elements.question_id.value;
    let current_question_nb = form.elements.current_question_nb.value;
    let nb_of_questions = form.elements.nb_of_questions.value;
    let ids_list = form.elements.ids_list.value;
    let score = form.elements.score.value;
    let request = new Request("assisted_quizz", { headers: { 'X-CSRFToken': csrftoken }});
    var formData = new FormData();
	formData.append('options', options);
	formData.append('question_id', question_id);
	formData.append('current_question_nb', current_question_nb);
	formData.append('nb_of_questions', nb_of_questions);
	formData.append('ids_list', ids_list);
	formData.append('score', score);
	fetch(request, { method: "POST", mode: "same-origin", body: formData })
    .then(function(response) {

      if(response.status !== 200) {
        console.log("La requête n'a pas abouti.");
      }
      response.json().then(function(data) {
        status.textContent = "";
        verify.innerHTML = data.reponse + "<br>"
        verify.innerHTML += data.explications + "<br>"
        verify.innerHTML += data.eliminatoire + "<br>"
        const thescore = data.score;
        const last = data.last;
        nextButton(thescore, last);
      })
    })
  }
})
