function logvalidate() {
  var email = document.getElementById("email").value;
  var password = document.getElementById("password").value;

  if (email == "") {
    document.getElementById("email").placeholder = "please provide email";
    return false;
  }
  return true;
}
