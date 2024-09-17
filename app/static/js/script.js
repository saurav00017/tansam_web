
let navbar = document.querySelector(".navbar");

// sidebar open close js code
let navLinks = document.querySelector(".nav-links");
let menuOpenBtn = document.querySelector(".navbar .bx-menu");
let menuCloseBtn = document.querySelector(".nav-links .bx-x");
menuOpenBtn.onclick = function() {
navLinks.style.left = "0";
}
menuCloseBtn.onclick = function() {
navLinks.style.left = "-100%";
}
let htmlcssArrow = document.querySelectorAll(".htmlcss-arrow");

for (let i = 0; i < htmlcssArrow.length; i++) {
  htmlcssArrow[i].addEventListener("click", (e) => {
    let htmlcssSubmenu = htmlcssArrow[i].nextElementSibling;
    // let styleCheck = htmlcssSubmenu.querySelector(".sub-menu");
    // console.log(styleCheck.style);
    // if ()
    htmlcssSubmenu.classList.toggle("checked");
    // document.querySelector(".sub-menu").style.display = "block";
    console.log(htmlcssSubmenu);
    // console.log(document.querySelector(".sub-menu").style.display);
    // htmlcssSubmenu.classList.toggle("d-block");
  });
}
// htmlcssArrow.onclick = function() {
//  navLinks.classList.toggle("show1");
// }
