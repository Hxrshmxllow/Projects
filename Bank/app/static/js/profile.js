function insertProfileDiv() {
    const navHTML = `
        <img src="static/img/profile/profileDivImg.png" id="safe-secure">
        <img src="static/img/profile/profile-picture.jpg" id="profile-picture">
    `;

    document.querySelectorAll('.profileDiv').forEach(container => {
        container.innerHTML = navHTML;
    });
}

document.addEventListener("DOMContentLoaded", insertProfileDiv);