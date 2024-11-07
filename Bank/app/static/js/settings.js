document.getElementById('profilePicture').addEventListener('change', async (event) => {
    event.preventDefault(); 
    var file    = document.querySelector('input[type=file]').files[0];
    var reader  = new FileReader();
    reader.onloadend = function () {
        document.getElementById("upload").src = reader.result;
    }
    if (file) {
        reader.readAsDataURL(file);
    } else {
        document.getElementById("upload").src = "";
    }
});


