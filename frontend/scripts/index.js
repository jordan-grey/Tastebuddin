/* 
File: index.js
Purpose:
  Controls login-dependent UI visibility on page load. Checks for an existing
  user ID in localStorage and toggles between the "logged in" and "logged out"
  sections of the page accordingly.
System Role:
  Ensures correct UI is shown before or without loading any backend resources.
Edited Last: 2025-12-04
Authors: Sarah
Uses:
  - localStorage — checks 'tastebuddin_user_id' for session state.
  - HTML elements with IDs: #logged-in and #logged-out.
  - API_BASE (currently pointing to localhost) reserved for future API calls.
Notes:
  - This script performs no authentication itself; it only checks stored state.
*/

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