document.getElementById('add_sentence_form').addEventListener('submit', function(e) {
    const criminalId = this.getAttribute('data-criminal-id');
    addSentence(e, criminalId);
});

document.getElementById('add_crime_form').addEventListener('submit', function(e) {
    const criminalId = this.getAttribute('data-criminal-id');
    if (checkAtLeastOneCheckbox(e)) {
        addCrime(e, criminalId);
    }
});

async function addCrime(e, criminalId) {
    e.preventDefault();
    const form = e.target;
    const charge_codes = Array.from(form.elements.charges).filter(charge => charge.checked).map(charge => charge.value);
    const fine = form.elements.fine.value;
    const amount_paid = form.elements.amount_paid.value;
    const payment_due_date = form.elements.payment_due_date.value;
    const court_fee = form.elements.court_fee.value;
    const res = await fetch(`/crimes`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            criminal_id: criminalId,
            charge_codes,
            fine,
            amount_paid,
            payment_due_date,
            court_fee
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

function checkAtLeastOneCheckbox(e) {
    e.preventDefault();
    const checkboxes = document.querySelectorAll('input[name="charges"]:checked');
    if (checkboxes.length === 0) {
        alert('Please select at least one charge code.');
        return false;
    }
    return true;
}

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