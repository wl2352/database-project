document.getElementById('add_officer_form').addEventListener('submit', function(e) {
    addOfficer(e);
});

async function addOfficer(e) {
    e.preventDefault();
    const form = e.target;

    const name = form.elements.name.value;
    const precinct = form.elements.precinct.value;
    const status = form.elements.status.checked;
    const add_phone = form.elements.add_phone.value;

    const res = await fetch(`/officers`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            name,
            precinct,
            status,
            add_phone
        }),
    })
    const data = await res.json();
    if (!res.ok) {
        alert(data.message)
    }
    else {
        // redirect to officer page
        window.location.href = `/officer/${data.badge_no}`;
    }
    
}
