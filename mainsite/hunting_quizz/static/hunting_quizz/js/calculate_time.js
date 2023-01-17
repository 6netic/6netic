
const timertag = document.getElementById('time_value');
let t = Number(document.getElementById("current_time").value);
setInterval(function () {
  t += 1;
  timertag.textContent = t;
}, 1000)
