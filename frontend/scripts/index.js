const API_BASE = "http://localhost:5001";


const userID = localStorage.getItem("tastebuddin_user_id");
document.addEventListener("DOMContentLoaded", () => {
    if (userID) {
        // For someone who is logged in
        // Hide logged out
        document.getElementById("logged-out").style.display = "none";
        // Show logged in
        document.getElementById("logged-in").style.display = "block";
        return;

    } else {
        // For someone who is logged out
        // Show logged out
        document.getElementById("logged-out").style.display = "block";
        // Hide logged in
        document.getElementById("logged-in").style.display = "none";
        return;
        
    }
});