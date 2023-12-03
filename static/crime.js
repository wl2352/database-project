document.getElementById('add_appeal_form').addEventListener('submit', function(e) {
    const crimeId = this.getAttribute('data-crime-id');
    addAppeal(e, crimeId);
});

async function addAppeal(e, crimeId) {
    e.preventDefault();
    const form = e.target;
    const filing_date = form.elements.filing_date.value;
    const hearing_date = form.elements.hearing_date.value;
    const appeal_status = form.elements.appeal_status.value;
    const res = await fetch(`/appeals`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            crime_id: crimeId,
            filing_date: filing_date,
            hearing_date: hearing_date,
            appeal_status: appeal_status,
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