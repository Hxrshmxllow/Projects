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
            <div class="flex md:order-2 space-x-3 md:space-x-0 rtl:space-x-reverse">
                <a href="${homeUrl}">
                    <button type="button" class="text-white  focus:ring-4 focus:outline-none font-medium rounded-lg text-sm px-4 py-2 text-center"
                     style="background-color: #07003b;">
                     Sign Out</button>
                </a>
                <button data-collapse-toggle="navbar-sticky" type="button" class="inline-flex items-center p-2 w-10 h-10 justify-center text-sm text-gray-500 rounded-lg md:hidden hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-200 dark:text-gray-400 dark:hover:bg-gray-700 dark:focus:ring-gray-600" aria-controls="navbar-sticky" aria-expanded="false">
                    <span class="sr-only">Open main menu</span>
                    <svg class="w-5 h-5" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 17 14">
                        <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M1 1h15M1 7h15M1 13h15"/>
                    </svg>
                </button>
            </div>
            <div class="items-center justify-between hidden w-full md:flex md:w-auto md:order-1" id="navbar-sticky">
                <ul class="flex flex-col p-4 md:p-0 mt-4 font-medium border border-gray-100 rounded-lg md:space-x-8 rtl:space-x-reverse md:flex-row md:mt-0 md:border-0 dark:border-gray-700">
                    <li><a id="homeLink" href="${adminHomeUrl}" class="block px-4 py-2 text-gray-900 hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white" style="color: #07003b;">Home</a></li>
                    <li><a id="ordersLink" href="${ordersUrl}" class="block px-4 py-2 text-gray-900 hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white" style="color: #07003b;">Orders</a></li>
                    <li><a id="inventoryLink" href="${inventoryUrl}" class="block px-4 py-2 text-gray-900 hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white" style="color: #07003b;">Manage Inventory</a></li>
                    <li><a id="upcLink" href="${upcUrl}" class="block px-4 py-2 text-gray-900 hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white" style="color: #07003b;">UPC Lookup</a></li>
                </ul>
            </div>
        </div>
    `;
    document.body.prepend(nav);  
    highlightActiveLink();
}

function highlightActiveLink() {  
    document.querySelectorAll("li a").forEach(link => {
        link.classList.remove(
            "text-white", "bg-blue-700", "hover:bg-blue-800", 
            "focus:ring-4", "focus:outline-none", "focus:ring-blue-300", 
            "font-medium", "rounded-lg", "text-sm", "px-4", "py-2", 
            "text-center", "dark:bg-blue-600", "dark:hover:bg-blue-700", 
            "dark:focus:ring-blue-800"
        );
        link.classList.add(
            "text-gray-900", "rounded", "hover:bg-gray-100", 
            "md:hover:bg-transparent", "md:border-0", "md:hover:text-blue-700", 
            "md:p-0", "md:w-auto", "dark:text-white", "md:dark:hover:text-blue-500", 
            "dark:focus:text-white", "dark:border-gray-700", "dark:hover:bg-gray-700", 
            "md:dark:hover:bg-transparent"
        );
    });
}
