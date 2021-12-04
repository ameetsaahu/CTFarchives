const log = document.getElementById('input');

document.addEventListener('keypress', handleChars);
document.addEventListener('keydown', handleBackspace);
var counter = 0;
var cursor  = 0;
function handleChars(e) {
    element = document.getElementById('input');
    if (e.keyCode == 91){
        return;
    }

    if (counter == 0){
        element.innerText = String.fromCharCode(e.keyCode);
        cursor++;
        counter++;
        return;
    }
    
    if (e.keyCode == 13){ // Enter
        if (check(element.innerText) == 0){
            element.innerText = "Correct";
        } else {
            element.innerText = "Wrong";
        }
        counter = 0;
        return;
    }
    element.innerText += String.fromCharCode(e.keyCode);
    cursor++;
    counter++;
}

function handleBackspace(e){
    element = document.getElementById('input');
    if (counter == 0){
        if (e.keyCode == 8){
            element.innerText = "";
            return;
        }
    }
    if (e.keyCode == 8){
        if (counter < 1){
            return;
        }
        element.innerText = element.innerText.substring(0, element.innerText.length - 1);
        counter--;
        return;
    }
}

function check(input){
    var enc = [
        0x14, 0x09, 0x17, 0x02, 0x09, 0x04, 0x5a, 0x0c,
        0x38, 0x42, 0x17, 0x29, 0x17, 0x17, 0x05, 0x0c,
        0x1c, 0x14, 0x1b, 0x0b, 0x11, 0x18
    ]

    xored = []

    for (var i = 0; i < 22; i++){
        xored.push(enc.charCodeAt(i) ^ "reversing".charCodeAt(i % 9));
    }

    var res = 0;
    for (var i = 0; i < 22; i++){
        res += (xored[i] ^ enc[i]);
    }

    return res;
}
