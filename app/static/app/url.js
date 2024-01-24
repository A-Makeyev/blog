let header = document.querySelector("header");
let link = document.querySelector(".links");
let main = document.querySelector("main");
main.style.paddingTop = header.offsetHeight + "px";

function menu() {
  link.classList.toggle("active");
}

function toggleDiv(a) {
  a = a.parentNode.parentNode.parentNode
  replybox = a.querySelector('.comment-box')
  if (replybox.style.display === "none") {
    replybox.style.display = "block";
  } else {
    replybox.style.display = "none";
  }
}
