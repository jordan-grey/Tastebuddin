const API_BASE = "http://localhost:5001";


const userID = localStorage.getItem("tastebuddin_user_id");
let signin_button= document.querySelector("#sign-in-out-button");
const username = "jimmy jone bow"

if (userID) {
    //For someone who is logged in
    signin_button.innerHTML = "Sign Out"
    if (document.getElementById("sign-in-out-button").onclick) {
        //TODO: implement logout?
    }
    let main_body= document.querySelector("#main-body");
    main_body.innerHTML = `
    <h1>Tastebuddin</h1>
    <p>Welcome ` + username + `!</p>
    
    <div class="btn">
        <button id="sign-in-out-button"></button>
    </div>
    <p>THIS IS DIFFERENT THAN THE OTHER PAGE</p>
    `;
    // Swipy button reveal
    // Logout button id="sign-in-out-button"
} else {
    // For someone who is logged out
    // Log in button id="sign-in-out-button"
    signin_button.innerHTML = "Sign In/Log In";
    if (document.getElementById("sign-in-out-button").onclick) {
        window.location.href = "sign-in.html"; // changed
    }
    

    // Describe how amazing it is *wiggles eyebrows*

}