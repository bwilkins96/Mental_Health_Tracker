// SWDV 620: Web Applications
// Script for changing circle colors on index page based on average scores

function changeCircleColor(circle) {
    const pEle = circle.querySelector('p');
    const avg = Number(pEle.innerText);
    let color = '';

    if (!avg) {
        return
    } else if (avg < 2) {
        color = 'indianred';
    } else if (avg < 3) {
        color = 'lightsalmon';
    } else if (avg < 4) {
        color = 'aquamarine';
    } else {
        color = 'springgreen';
    }

    circle.style.backgroundColor = color;
}

function main() {
    const avgCircles = document.querySelectorAll('.circle');

    for(let i = 0; i < avgCircles.length; i++) {
        changeCircleColor(avgCircles[i]);
    }

    circle = avgCircles[0];
}

main()