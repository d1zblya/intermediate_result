window.onload = function () {
    document.body.classList.add('loaded_hiding');
    window.setTimeout(function () {
        document.body.classList.add('loaded');
        document.body.classList.remove('loaded_hiding');
    }, 500);
}

function onEntry(entry) {
    entry.forEach(change => {
        if (change.isIntersecting) {
            change.target.classList.add('show')
        }
    })
}

let options = {threshold: [0.5]};
let observer = new IntersectionObserver(onEntry, options)
let elements = document.querySelectorAll('.animation, .animation-left, .animation-right')
console.log(elements)
for (let elm of elements) {
    observer.observe(elm);
}

var modal0 = new bootstrap.Modal(document.getElementById('review0'), {
    keyboard: false
});
var modal1 = new bootstrap.Modal(document.getElementById('review1'), {
    keyboard: false
});
console.log(modal0);
console.log(modal1);
let time = 2000;
document.addEventListener('DOMContentLoaded', (event) => {
    setTimeout(function() {
        modal0.show();
    }, time);
});


const onLoad = (e) => {
    e.preventDefault();

    setTimeout(() => window.location.replace(e.target.href), 1000)
}
$(document).ready(function () {
    $('.readmore-content').readmore({
        moreLink: '<a href="#">Читать далее</a>',
        lessLink: '<a href="#">Скрыть</a>',
        collapsedHeight: 80,
    });
});
