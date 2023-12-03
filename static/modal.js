const modals = document.getElementsByClassName('modal');
const btns = document.getElementsByClassName('modal-btn');
const spans = document.getElementsByClassName("close");

let openModal = null; // keep track of the open modal

for (let i = 0; i < btns.length; i++) {
    btns[i].onclick = function() {
        modals[i].style.display = "block";
        openModal = modals[i]; // This modal is now open
    }

    spans[i].onclick = function() {
        modals[i].style.display = "none";
        openModal = null; // No modal is open
    }
}

window.onclick = function(event) {
    // theres an open modal and the click was outside of it, close it
    if (openModal && event.target == openModal) {
        openModal.style.display = "none";
        openModal = null;
    }
}

async function deletePrompt(type, id) {
    let inp;
    switch(type) {
        case 'criminal':
            inp = confirm('Delete this criminal? All related data will be deleted.')
            if (inp) {
                const res = await fetch(`/criminal/${id}`, {
                    method: 'DELETE'
                });
                if (res.ok) {
                    window.location.href = '/criminals';
                }
                else {
                    alert('Something went wrong')
                }
            }
            break;
        case 'crime':
            inp = confirm('Delete this crime? All related data will be deleted.')
            if (inp) {
                const res = await fetch(`/crime/${id}`, {
                    method: 'DELETE'
                });
                if (res.ok) {
                    // change this to /crimes
                    window.location.href = '/criminals';
                }
                else {
                    alert('Something went wrong')
                }
            }
            break;
        case 'sentence':
            inp = confirm('Delete this sentence?')
            if (inp) {
                const res = await fetch(`/sentence/${id}`, {
                    method: 'DELETE'
                });
                if (res.ok) {
                    // change this to /sentences
                    window.location.href = '/criminals';
                }
                else {
                    alert('Something went wrong')
                }
            }
            break;
        case 'officer':
            inp = confirm('Delete this officer? All related date will be deleted.');
            if (inp) {
                const res = await fetch(`/officer/${id}`, {
                    method: 'DELETE'
                });
                if (res.ok) {
                    window.location.href = '/officers';
                }
                else {
                    alert('Something went wrong')
                }
            }
            break;
    }
}