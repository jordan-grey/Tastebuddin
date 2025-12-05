/* 
File: nav-dropdown.js
Purpose:
  Handles navigation bar behavior for the Tastebuddin interface, including:
  - Responsive mobile menu toggle
System Role:
  Shared front-end utility script used across multiple pages. Provides user
  session management and controls the responsive navigation dropdown.
Edited Last: 2025-12-04
Authors: Sarah
Modifications:
  - Added responsive hamburger menu toggle
Uses:
  - HTML element #myTopnav for responsive class toggling
*/


/* Toggle between adding and removing the "responsive" class to topnav when the user clicks on the icon */

function myFunction() {
  var x = document.getElementById("myTopnav");
  if (x.className === "topnav") {
    x.className += " responsive";
  } else {
    x.className = "topnav";
  }
} 