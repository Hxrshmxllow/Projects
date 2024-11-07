function createFooter() {
    const footerHTML = `
      <div class="bg-gray-900 text-white py-8">
        <div class="container mx-auto grid grid-cols-2 md:grid-cols-4 gap-8 px-4">
          <div>
            <h2 class="font-bold mb-4">OUR PRODUCT</h2>
            <hr class="w-8 border-t-2 border-[#e02575] mb-4">
            <ul class="space-y-2">
              <li><a href="${womensFragranceUrl}" class="hover:text-[#e02575]">Women's Fragrance</a></li>
              <li><a href="${womensGiftSetUrl}" class="hover:text-[#e02575]">Women's Gift Sets</a></li>
              <li><a href="${womensDeodorantUrl}" class="hover:text-[#e02575]">Women's Deodorants</a></li>
              <li><a href="${mensFragranceUrl}" class="hover:text-[#e02575]">Men's Fragrance</a></li>
              <li><a href="${mensGiftSetUrl}" class="hover:text-[#e02575]">Men's Gift Sets</a></li>
              <li><a href="${mensAfterShaveUrl}" class="hover:text-[#e02575]">Men's After Shave </a></li>
              <li><a href="${mensDeodorantUrl}" class="hover:text-[#e02575]">Men's Deodorants</a></li>
              <li><a href="#" class="hover:text-[#e02575]">Deodorant</a></li>
            </ul>
          </div>
          <div>
            <h2 class="font-bold mb-4">INFORMATION</h2>
            <hr class="w-8 border-t-2 border-[#e02575] mb-4">
            <ul class="space-y-2">
              <li><a href="${aboutUsUrl}" class="hover:text-[#e02575]">About Us</a></li>
              <li><a href="${deliveryUrl}" class="hover:text-[#e02575]">Delivery</a></li>
              <li><a href="#" class="hover:text-[#e02575]">Returns</a></li>
              <li><a href="#" class="hover:text-[#e02575]">Payment</a></li>
              <li><a href="#" class="hover:text-[#e02575]">Tax Policy</a></li>
              <li><a href="#" class="hover:text-[#e02575]">Privacy Policy</a></li>
              <li><a href="${faqUrl}" class="hover:text-[#e02575]">FAQ'S</a></li>
              <li><a href="#" class="hover:text-[#e02575]">Contact Us</a></li>
            </ul>
          </div>
  
          <!-- My Account Section -->
          <div>
            <h2 class="font-bold mb-4">MY ACCOUNT</h2>
            <hr class="w-8 border-t-2 border-[#e02575] mb-4">
            <ul class="space-y-2">
              <li><a href="#" class="hover:text-[#e02575]">Login</a></li>
              <li><a href="#" class="hover:text-[#e02575]">Register</a></li>
              <li><a href="#" class="hover:text-[#e02575]">My Account</a></li>
              <li><a href="#" class="hover:text-[#e02575]">Wish List</a></li>
              <li><a href="#" class="hover:text-[#e02575]">Don’t See It Request it</a></li>
            </ul>
          </div>
  
          <!-- Need Help Section -->
          <div>
            <h2 class="font-bold mb-4">NEED HELP?</h2>
            <hr class="w-8 border-t-2 border-[#e02575] mb-4">
            <ul class="space-y-2">
              <li><a href="tel:7328957941" class="flex items-center space-x-2 hover:text-[#e02575]">
                <span>📞</span><span>7328957941</span>
              </a></li>
              <li><a href="mailto:noblemart@gmail.com" class="flex items-center space-x-2 hover:text-[#e02575]">
                <span>📧</span><span>noblemart@gmail.com</span>
              </a></li>
              <li class="flex items-center space-x-2">
                <span>⏰</span><span>MON-FRI : 9:30 AM – 5:00 PM Eastern Standard Time</span>
              </li>
            </ul>
            <div class="flex space-x-4 mt-4">
              <a href="#" class="hover:text-[#e02575]">🐦</a>
              <a href="#" class="hover:text-[#e02575]">📘</a>
              <a href="#" class="hover:text-[#e02575]">📸</a>
            </div>
          </div>
        </div>
  
        <div class="border-t border-gray-700 my-8"></div>
  
        <!-- Footer Bottom Section -->
        <div class="container mx-auto text-center space-y-4">
          <img src="path/to/logo.png" alt="NobleMart Logo" class="mx-auto mb-4">
          <p class="text-sm text-gray-400">&copy; 2024 noblemart.net All rights reserved</p>
  
          <div class="flex justify-center space-x-4">
            <span class="flex items-center space-x-1 text-sm">
              <span>🔒</span><span>Secure Shopping</span>
            </span>
            <span class="flex items-center space-x-1 text-sm">
              <span>👍</span><span>Excellent Customer Service</span>
            </span>
            <span class="flex items-center space-x-1 text-sm">
              <span>🏅</span><span>Accredited Business</span>
            </span>
          </div>
  
          <div class="flex justify-center space-x-4 mt-4">
            <img src="path/to/paypal.png" alt="PayPal" class="h-6">
            <img src="path/to/visa.png" alt="Visa" class="h-6">
            <img src="path/to/mastercard.png" alt="MasterCard" class="h-6">
            <img src="path/to/discover.png" alt="Discover" class="h-6">
            <img src="path/to/amex.png" alt="American Express" class="h-6">
          </div>
        </div>
      </div>
    `;
    document.body.insertAdjacentHTML('beforeend', footerHTML);
  }
  export { createFooter };
  