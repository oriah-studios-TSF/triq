const toast = document.getElementById("toast");
const toastMessage = document.getElementById("toast-message");

// Display a toast notification
function showToast(message, backgroundColor) {
    toastMessage.textContent = message;
    toast.style.backgroundColor = backgroundColor;
    toast.classList.add("show");

    setTimeout(function () {
        toast.classList.remove("show");
    }, 3000);
}