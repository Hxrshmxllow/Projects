export function createNavbar() {
    const nav = document.createElement('nav');
    nav.className = "fixed w-full z-20 top-0 start-0 border-b";
    nav.style.backgroundColor = "#dfdfdf";
    nav.style.boxShadow = "0px 4px 10px rgba(0, 0, 0, 0.2)";
    nav.style.padding = "0px 0"; 
    nav.innerHTML = `
        <div class="max-w-screen-xl flex flex-wrap items-center justify-between mx-auto p-4">
            <a href="${homeUrl}" class="flex items-center space-x-3 rtl:space-x-reverse">
                <img src="${logoUrl}" class="h-20" alt="NobleMart Logo">
            </a>
            <div class="flex md:order-2 space-x-6 md:space-x-3 rtl:space-x-reverse">
                <a href="${signInUrl}">
                    <button type="button" class="text-white font-medium rounded-lg text-sm px-4 py-2 text-center"
                        style="background-color: #07003b;">
                        Sign In
                    </button>
                </a>
                <a href="${cartUrl}">
                    <button type="button" class="flex items-center text-white font-medium rounded-lg text-sm px-4 py-2 space-x-2"
                        style="background-color: #07003b;">
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13l-1.5 8h11l-1.5-8M10 21a2 2 0 100-4 2 2 0 000 4zM18 21a2 2 0 100-4 2 2 0 000 4z"/>
                        </svg>
                        <span>Cart</span>
                    </button>
                </a>
            </div>
            <div class="items-center justify-center w-full md:flex md:w-auto md:order-1" id="navbar-sticky">
                <ul class="flex flex-col p-4 md:p-0 mt-4 font-medium border border-gray-100 rounded-lg md:space-x-8 rtl:space-x-reverse md:flex-row md:mt-0 md:border-0">
                    <li>
                        <a href="${homeUrl}" class="block py-2 px-3 rounded md:bg-transparent md:p-0" aria-current="page" style="color: #07003b;">Home</a>
                    </li>
                    <li>
                        <button id="mensDropdownNavbarLink" data-dropdown-toggle="mensDropdown" class="flex items-center justify-between w-full py-2 px-3 rounded hover:bg-opacity-80 md:hover:bg-transparent md:border-0 md:p-0 md:w-auto" style="color: #07003b;">Men's Collection
                            <svg class="w-2.5 h-2.5 ms-2.5" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 10 6">
                                <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m1 1 4 4 4-4"/>
                            </svg>
                        </button>
                        <div id="mensDropdown" class="z-10 hidden font-normal divide-y divide-gray-100 rounded-lg shadow w-44" style="background-color: #07003b;">
                            <ul class="py-2 text-sm" aria-labelledby="dropdownLargeButton">
                                <li><a href="${mensFragranceUrl}" class="block px-4 py-2 hover:bg-opacity-80 text-white">Fragrances</a></li>
                                <li><a href="${mensDeodorantUrl}" class="block px-4 py-2 hover:bg-opacity-80 text-white">Deodorants</a></li>
                                <li><a href="${mensAfterShaveUrl}" class="block px-4 py-2 hover:bg-opacity-80 text-white">After Shave</a></li>
                                <li><a href="${mensGiftSetUrl}" class="block px-4 py-2 hover:bg-opacity-80 text-white">Gift Sets</a></li>
                            </ul>
                        </div>
                    </li>
                    <li>
                        <button id="womensDropdownNavbarLink" data-dropdown-toggle="womensDropdown" class="flex items-center justify-between w-full py-2 px-3 rounded hover:bg-opacity-80 md:hover:bg-transparent md:border-0 md:p-0 md:w-auto" style="color: #07003b;">Women's Collection
                            <svg class="w-2.5 h-2.5 ms-2.5" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 10 6">
                                <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m1 1 4 4 4-4"/>
                            </svg>
                        </button>
                        <div id="womensDropdown" class="z-10 hidden font-normal divide-y divide-gray-100 rounded-lg shadow w-44" style="background-color: #07003b;">
                            <ul class="py-2 text-sm" aria-labelledby="dropdownLargeButton">
                                <li><a href="${womensFragranceUrl}" class="block px-4 py-2 hover:bg-opacity-80 text-white">Fragrances</a></li>
                                <li><a href="${womensDeodorantUrl}" class="block px-4 py-2 hover:bg-opacity-80 text-white">Deodorants</a></li>
                                <li><a href="${womensGiftSetUrl}" class="block px-4 py-2 hover:bg-opacity-80 text-white">Gift Sets</a></li>
                            </ul>
                        </div>
                    </li>
                    <li>
                        <button id="dropdownNavbarLink" data-dropdown-toggle="dropdownNavbar" class="flex items-center justify-between w-full py-2 px-3 rounded hover:bg-opacity-80 md:hover:bg-transparent md:border-0 md:p-0 md:w-auto" style="color: #07003b;">Shop by Brands
                            <svg class="w-2.5 h-2.5 ms-2.5" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 10 6">
                                <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m1 1 4 4 4-4"/>
                            </svg>
                        </button>
                        <div id="dropdownNavbar" class="z-10 hidden font-normal divide-y divide-gray-100 rounded-lg shadow w-44" style="background-color: #07003b;">
                            <ul id="brandsList" class="py-2 text-sm text-white" aria-labelledby="dropdownNavbarLink">
                                <!-- Brands populated here by JavaScript -->
                            </ul>
                        </div>
                    </li>
                </ul>
            </div>
        </div>
    `;

    document.body.prepend(nav);

    fetch('/api/brands')
    .then(response => response.json())
    .then(brands => {
        const brandsList = document.getElementById('brandsList');
        brands.forEach(brand => {
            const listItem = document.createElement('li');
            listItem.innerHTML = `<a href="/brandsendpoint?brand=${encodeURIComponent(brand)}" class="block px-4 py-2 hover:bg-opacity-80 text-white">${brand}</a>`;
            brandsList.appendChild(listItem);
        });
    })
    .catch(error => console.error('Error fetching brands:', error));
}
