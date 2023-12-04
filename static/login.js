const form = document.getElementById('login_form');

form.addEventListener('submit', handleLogin);

async function handleLogin(e) {
    e.preventDefault();
    const form = e.target;

    const username = form.elements.username.value;
    const password = form.elements.password.value;
    const remember = form.elements.remember.checked;


    const res = await fetch(`/login`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            username,
            password,
            remember
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