let DateEl = document.querySelector(".date--span");

let date = new Date().toLocaleDateString();
DateEl.innerHTML = `Date: ${date}`;
