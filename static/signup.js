const form = document.getElementById('signup_form');

form.addEventListener('submit', handleSignup);

async function handleSignup(e) {
    e.preventDefault();
    const form = e.target;

    const username = form.elements.username.value;
    const password = form.elements.password.value;
    const role = form.elements.role.value;


    const res = await fetch(`/signup`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            username,
            password,
            role
        }),
    })
    const data = await res.json();
    if (!res.ok) {
        alert(data.message)
    }
    else {
        window.location.href = `/criminals`;
    }
}