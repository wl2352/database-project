document.getElementById('add_sentence_form').addEventListener('submit', function(e) {
    const criminalId = this.getAttribute('data-criminal-id');
    addSentence(e, criminalId);
});

async function addSentence(e, criminalId) {
    e.preventDefault();
    const form = e.target;
    const start_date = form.elements.start_date.value;
    const end_date = form.elements.end_date.value;
    const num_violations = form.elements.num_violations.value;
    const type = form.elements.type.value;
    const res = await fetch(`/sentences`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            criminal_id: criminalId,
            start_date: start_date,
            end_date: end_date,
            num_violations: num_violations,
            type: type
        }),
    })
    if (!res.ok) {
        const data = await res.json();
        alert(data.message)
    }
    else {
        window.location.reload();
    }
    
}