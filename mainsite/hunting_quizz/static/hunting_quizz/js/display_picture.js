
function random_image(min, max) {
  min = Math.ceil(1);
  max = Math.floor(3);
  let number = Math.floor(Math.random() * (max - min + 1) + min);
  return number
}
random_no = random_image(1, 3);

function display_image(div_name, path_folder) {
  let thumbnail = document.getElementById(div_name);
  let image = document.createElement("img");
  image.src = path_folder + random_no.toString() + ".jpg";
  thumbnail.appendChild(image);
}
display_image(div_name, path_folder);
