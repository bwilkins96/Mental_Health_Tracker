// SWDV 620: Web Applications
// Script for changing background color of list elements based on average log value 

// Returns average of mental health, environment, and sleep quality ratings for log
function parseAvg(li){
    const inner = li.innerText;
    
    const mh_avg = Number(inner[15]);
    const env_avg = Number(inner[33]);
    const sleep_avg = Number(inner[45]);

    return (mh_avg + env_avg + sleep_avg) / 3;
}

// Sets the background of the li element based on the passed-in avg
function setBackground(li, avg) {
    let color = '';

    if (avg < 2) {
        color = 'lightcoral';
    } else if (avg < 3) {   
        color = 'lightsalmon';
    }  else if (avg < 4) {
        color = 'aquamarine';
    } else {
        color = 'springgreen';
    }

    li.style.backgroundColor = color;
}

function main() {
    const liEles = document.querySelectorAll('li');
    
    for(let i = 0; i < liEles.length; i++) {
        const li = liEles[i];
        const avg = parseAvg(liEles[i]);

        setBackground(li, avg);
    }
}

main();