
function nextButton(thescore, last) {
  // Erase 'Je Valide' button
  const checkBtn = document.getElementById("valid");
  checkBtn.innerHTML = "";
  // Creates formular with 'Question suivante' button
  const formular = document.createElement('form');
  formular.setAttribute("method", "GET");
  formular.setAttribute("action", "assisted_quizz");
  // Creates 'Question suivante' button
  const nextBtn = document.createElement("button");
  nextBtn.setAttribute("class", "btn btn-success validateBtn");
  if (last === true) {
    nextBtn.textContent = "Afficher les résultats";
  } else {
    nextBtn.textContent = "Question suivante";
  }
  // Creates 'ids_list' input
  const ids_list = document.createElement("input");
  ids_list.setAttribute("type", "hidden");
  ids_list.setAttribute("name", "ids_list");
  ids_list.setAttribute("value", form.elements.ids_list.value);
  // Creates 'question_id' input
  const question_id = document.createElement("input");
  question_id.setAttribute("type", "hidden");
  question_id.setAttribute("name", "question_id");
  question_id.setAttribute("value", form.elements.question_id.value);
  // Creates 'score' input
  const score = document.createElement("input");
  score.setAttribute("type", "hidden");
  score.setAttribute("name", "score");
  score.setAttribute("value", thescore);
  // Creates 'current_question_nb' input
  const current_question_nb = document.createElement("input");
  current_question_nb.setAttribute("type", "hidden");
  current_question_nb.setAttribute("name", "current_question_nb");
  current_question_nb.setAttribute("value", form.elements.current_question_nb.value);
  // Creates 'nb_of_questions' input
  const nb_of_questions = document.createElement("input");
  nb_of_questions.setAttribute("type", "hidden");
  nb_of_questions.setAttribute("name", "nb_of_questions");
  nb_of_questions.setAttribute("value", form.elements.nb_of_questions.value);
  // Adds elements to the form
  formular.appendChild(nextBtn);
  formular.appendChild(ids_list);
  formular.appendChild(question_id);
  formular.appendChild(score);
  formular.appendChild(current_question_nb);
  formular.appendChild(nb_of_questions);
  // Adds the form to formtag tag
  const formtag = document.getElementById("formtag");
  formtag.appendChild(formular);
}
