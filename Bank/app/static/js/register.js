document.getElementById('registerForm').addEventListener('submit', async (event) => {
    event.preventDefault(); 
    const username = document.getElementById("Username").value;
    const password = document.getElementById("Password").value;

    try {
        const response = await fetch('/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, password })
        });

        if (response.ok) {
            const data = await response.json();
            localStorage.setItem('access_token', data.access_token);
            alert('Register successful!');
            window.location.href = '/settings';
        } else {
            const errorData = await response.json();
            alert(errorData.msg);
            window.location.replace('/register');
        }
    } catch (err) {
        alert('An error occurred. Please try again later.');
    }
});