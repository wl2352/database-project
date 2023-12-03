const modal = document.getElementsByClassName('modal')[0];
const btn = document.getElementsByClassName('edit')[0];
const span = document.getElementsByClassName("close")[0];

async function deletePrompt(type, id) {
    switch(type) {
        case 'criminal':
            const inp = confirm('Delete this criminal? All related data will be deleted.')
            if (inp) {
                const res = await fetch(`/criminal/${id}`, {
                    method: 'DELETE'
                });
                if (res.ok) {
                    window.location.href = '/criminals';
                }
                else {
                    prompt('something went wrong')
                }
            }
            break;
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