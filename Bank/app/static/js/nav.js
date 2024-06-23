function insertNav() {
    const navHTML = `
        <img src="static/img/nav/logo.png" class="logo">
        <div class="navItem" id="dashboard">
            <a href="/dashboard" onclick="nav('dashboard')">
                <img src="static/img/nav/dashboard.png" class="navLogo">
                Dashboard
            </a>
        </div>
        <div class="navItem" id="accounts">
            <a href="/accounts" onclick="nav('accounts')">
                <img src="static/img/nav/account.png" class="navLogo">
                Accounts
            </a>
        </div>
        <div class="navItem" id="myCards">
            <a href="/my-cards" onclick="nav('myCards')">
                <img src="static/img/nav/card.png" class="navLogo">
                My Cards
            </a>
        </div>
        <div class="navItem" id="fundTransfer">
            <a href="/fund-transfer" onclick="nav('fundTransfer')">
                <img src="static/img/nav/fundTransfer.png" class="navLogo">
                Fund Transfer
            </a>
        </div>
        <div class="navItem" id="payment">
            <a href="#" onclick="nav('payment')">
                <img src="static/img/nav/makePayment.png" class="navLogo">
                Make Payment
            </a>
        </div>
        <div class="navItem" id="settings">
            <a href="/settings" onclick="nav('settings')">
                <img src="static/img/nav/settings.png" class="navLogo">
                Settings
            </a>
        </div>
    `;

    document.querySelectorAll('.navDiv').forEach(container => {
        container.innerHTML = navHTML;
    });
}

document.addEventListener("DOMContentLoaded", insertNav);

function nav(id) {
    const navItems = ['dashboard', 'accounts', 'myCards', 'fundTransfer', 'payment', 'settings'];
    for (let i = 0; i < navItems.length; i++) {
        if (navItems[i] == id) {
            document.getElementById(navItems[i]).style.backgroundColor = "blue";
        } else {
            document.getElementById(navItems[i]).style.backgroundColor = "transparent";
        }
    }
}