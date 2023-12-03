const modal = document.getElementsByClassName('modal')[0];
const btn = document.getElementsByClassName('edit')[0];
const span = document.getElementsByClassName("close")[0];

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
    }
}

btn.onclick = function() {
    modal.style.display = "block";
}

span.onclick = function() {
    modal.style.display = "none";
}

window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}