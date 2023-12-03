const edit_officer_form = document.getElementById('edit_officer_form');
edit_officer_form.addEventListener('submit', async function(e) {
    const badge_no = this.getAttribute('data-officer-id');
    e.preventDefault();
    const form = e.target;

    const name = form.elements.name.value;
    const precinct = form.elements.precinct.value;
    const status = form.elements.status.checked;

    const phone = form.elements.phone.value;
    const phone_select = form.elements.phone_select.value;
    const delete_phone = form.elements.delete_phone.checked;
    const add_phone = form.elements.add_phone.value;

    const res = await fetch(`/officer/${badge_no}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            name,
            precinct,
            status,
            phone,
            phone_select,
            delete_phone,
            add_phone
        }),
    })
    if (!res.ok) {
        const data = await res.json();
        alert(data.message)
    }
    else {
        window.location.reload();
    }
});