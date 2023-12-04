document.getElementById('add_criminal_form').addEventListener('submit', function(e) {
    if (checkAtLeastOneCheckbox(e)) {
        addCriminal(e);
    }
});

async function addCriminal(e) {
    e.preventDefault();
    const form = e.target;
    // criminal info
    const name = form.elements.name.value;
    const violent_status = form.elements.violent_status.checked;
    const probation_status = form.elements.probation_status.checked;
    const add_alias = form.elements.add_alias.value;
    const add_address = form.elements.add_address.value;
    const add_phone = form.elements.add_phone.value;

    // crime info
    const charge_codes = Array.from(form.elements.charges).filter(charge => charge.checked).map(charge => charge.value);
    const fine = form.elements.fine.value;
    const amount_paid = form.elements.amount_paid.value;
    const payment_due_date = form.elements.payment_due_date.value;
    const court_fee = form.elements.court_fee.value;

    // sentence info
    const start_date = form.elements.start_date.value;
    const end_date = form.elements.end_date.value;
    const num_violations = form.elements.num_violations.value;
    const type = form.elements.type.value;

    const res = await fetch(`/criminals`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            name,
            violent_status,
            probation_status,
            add_alias,
            add_address,
            add_phone,
            charge_codes,
            fine,
            amount_paid,
            payment_due_date,
            court_fee,
            start_date,
            end_date,
            num_violations,
            type
        }),
    })
    const data = await res.json();
    if (!res.ok) {
        alert(data.message)
    }
    else {
        // redirect to criminal page
        console.log('criminal id is ', data.criminal_id);
        window.location.href = `/criminal/${data.criminal_id}`;
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