const first_nameE1 = document.querySelector("#first_name");
const last_nameE1 = document.querySelector("#last_name");
const emailEl = document.querySelector("#email");
const passwordEl = document.querySelector("#password");
const confirmPasswordEl = document.querySelector("#confirm_password");
const contactEl = document.querySelector("#contact");
const genderEl = document.querySelector("#gender");
const dobEl = document.querySelector("#dob");
const stateE1 = document.querySelector("#state");
const districtEl = document.querySelector("#district");

const form = document.querySelector("#signup");

const Checkfirst_nameE1 = () => {
  let valid = false;
  const first_name = first_nameE1.value.trim();
  if (!isRequired(first_name)) {
    // setErrorFor(first_nameE1, "First name is required");
    // document.getElementById("f-name").style.borderColor = "red";
    // document.getElementById("f-name").innerHTML = "Enter first_name";
    alert("First name is required");
  } else if (!isLength(first_name, 3)) {
    // document.getElementById("f-name").style.borderColor = "red";
    // document.getElementById("f-name").innerHTML =
    //   "First name must be at least 3 characters";
    alert("First name must be at least 3 characters");
  } else {
    setSuccessFor(first_nameE1);
    valid = true;
  }
  return valid;
};

const Checklast_nameE1 = () => {
  let valid = false;
  const last_name = last_nameE1.value.trim();
  if (!isRequired(last_name)) {
    // setErrorFor(last_nameE1, "Last name is required");
    // document.getElementById("l-name").style.borderColor = "red";
    // document.getElementById("l-name").innerHTML = "Enter last_name";
    alert("Last name is required");
  } else {
    setSuccessFor(last_nameE1);
    valid = true;
  }
  return valid;
};

const checkEmail = () => {
  let valid = false;
  const email = emailEl.value.trim();
  if (!isRequired(email)) {
    // showError(emailEl, "Email cannot be blank.");
    // document.getElementById("e").style.borderColor = "red";
    // document.getElementById("e").innerHTML = "Enter email";
    alert("Email cannot be blank.");
  } else if (!isEmailValid(email)) {
    // showError(emailEl, "Email is not valid.");
    // document.getElementById("e").style.borderColor = "red";
    // document.getElementById("e").innerHTML = "Enter valid email";
    alert("Email is not valid.");
  } else {
    showSuccess(emailEl);
    valid = true;
  }
  return valid;
};

const checkPassword = () => {
  let valid = false;

  const password = passwordEl.value.trim();

  if (!isRequired(password)) {
    // showError(passwordEl, "Password cannot be blank.");
    // document.getElementById("p").style.borderColor = "red";
    // document.getElementById("p").innerHTML = "Enter password";
    alert("Password cannot be blank.");
  } else if (!isPasswordSecure(password)) {
    // showError(
    //   passwordEl,
    //   "Password must has at least 8 characters that include at least 1 lowercase character, 1 uppercase characters, 1 number, and 1 special character in (!@#$%^&*)"
    // );
    // document.getElementById("p").style.borderColor = "red";
    // document.getElementById("p").innerHTML =
    //   "Password must has at least 8 characters that include at least 1 lowercase character, 1 uppercase characters, 1 number, and 1 special character in (!@#$%^&*)";
    alert(
      "Password must has at least 8 characters that include at least 1 lowercase character, 1 uppercase characters, 1 number, and 1 special character in (!@#$%^&*)"
    );
  } else {
    showSuccess(passwordEl);
    valid = true;
  }

  return valid;
};

const checkConfirmPassword = () => {
  let valid = false;
  // check confirm password
  const confirmPassword = confirmPasswordEl.value.trim();
  const password = passwordEl.value.trim();

  if (!isRequired(confirmPassword)) {
    // showError(confirmPasswordEl, "Please enter the password again");
    // document.getElementById("cf").style.borderColor = "red";
    // document.getElementById("cf").innerHTML = "Enter confirm_password";
    alert("Please enter the password again");
  } else if (password !== confirmPassword) {
    // showError(confirmPasswordEl, "The password does not match");
    // document.getElementById("cf").style.borderColor = "red";
    // document.getElementById("cf").innerHTML = "The password does not match";
    alert("The password does not match");
  } else {
    showSuccess(confirmPasswordEl);
    valid = true;
  }

  return valid;
};

const CheckContact = () => {
  let valid = false;
  const contact = contactEl.value.trim();
  if (!isRequired(contact)) {
    // showError(contactEl, "Contact cannot be blank");
    // document.getElementById("ph").style.borderColor = "red";
    // document.getElementById("ph").innerHTML = "Enter contact";
    alert("Contact cannot be blank");
  } else if (!isContactValid(contact)) {
    // showError(contactEl, "Contact is not valid");
    // document.getElementById("ph").style.borderColor = "red";
    // document.getElementById("ph").innerHTML = "Enter valid contact";
    alert("Contact is not valid");
  } else {
    showSuccess(contactEl);
    valid = true;
  }
  return valid;
};

const Checkgender = () => {
  let valid = false;
  const gender = genderEl.value.trim();
  if (!isRequired(gender)) {
    // showError(genderEl, "Gender cannot be blank");
    // document.getElementById("g").style.borderColor = "red";
    // document.getElementById("g").innerHTML = "Enter gender";
    alert("gender cannot be blank.");
  } else {
    showSuccess(genderEl);
    valid = true;
  }
  return valid;
};

const Checkdob = () => {
  let valid = false;
  const dob = dobEl.value.trim();
  if (!isRequired(dob)) {
    // showError(dobEl, "DOB cannot be blank");
    // document.getElementById("d").style.borderColor = "red";
    // document.getElementById("d").innerHTML = "Enter dob";
    alert("DOB cannot be blank.");
  } else {
    showSuccess(dobEl);
    valid = true;
  }
  return valid;
};

const CheckState = () => {
  let valid = false;
  const state = stateEl.value.trim();
  if (!isRequired(state)) {
    // showError(stateEl, "State cannot be blank");
    // document.getElementById("s").style.borderColor = "red";
    // document.getElementById("s").innerHTML = "Enter state";
    alert("State cannot be blank.");
  } else {
    showSuccess(stateEl);
    valid = true;
  }
  return valid;
};

const CheckDistrict = () => {
  let valid = false;
  const district = districtEl.value.trim();
  if (!isRequired(district)) {
    // showError(districtEl, "District cannot be blank");
    // document.getElementById("d").style.borderColor = "red";
    // document.getElementById("d").innerHTML = "Enter district";
    alert("District cannot be blank.");
  } else {
    showSuccess(districtEl);
    valid = true;
  }
  return valid;
};

const isEmailValid = (email) => {
  const re =
    /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  return re.test(email);
};

const isPasswordSecure = (password) => {
  const re = new RegExp(
    "^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%^&*])(?=.{8,})"
  );
  return re.test(password);
};

// phone number validation
const isContactValid = (contact) => {
  const re = /^[0-9]{10}$/;
  return re.test(contact);
};

const isRequired = (value) => (value === "" ? false : true);
const isBetween = (length, min, max) =>
  length < min || length > max ? false : true;

const showError = (input, message) => {
  // get the form-field element
  const formField = input.parentElement;
  // add the error class
  formField.classList.remove("success");
  formField.classList.add("error");

  // show the error message
  const error = formField.querySelector("small");
  error.textContent = message;
};

const showSuccess = (input) => {
  // get the form-field element
  const formField = input.parentElement;

  // remove the error class
  formField.classList.remove("error");
  formField.classList.add("success");

  // hide the error message
  const error = formField.querySelector("small");
  error.textContent = "";
};

form.addEventListener("submit", function (e) {
  // prevent the form from submitting
  e.preventDefault();

  // validate fields
  let isEmailValid = checkEmail(),
    isPasswordValid = checkPassword(),
    isConfirmPasswordValid = checkConfirmPassword(),
    isContactValid = CheckContact(),
    isGenderValid = Checkgender(),
    isDobValid = Checkdob(),
    isFirstNameValid = Checkfirst_nameE1(),
    isLastNameValid = Checklast_nameE1(),
    isStateValid = CheckState(),
    isDistrictValid = CheckDistrict();

  let isFormValid =
    isEmailValid &&
    isPasswordValid &&
    isConfirmPasswordValid &&
    isContactValid &&
    isGenderValid &&
    isDobValid &&
    isFirstNameValid &&
    isLastNameValid &&
    isStateValid &&
    isDistrictValid;

  // submit to the server if the form is valid
  if (isFormValid) {
    // submit the form
    form.submit();
  }
});

const debounce = (fn, delay = 500) => {
  let timeoutId;
  return (...args) => {
    // cancel the previous timer
    if (timeoutId) {
      clearTimeout(timeoutId);
    }
    // setup a new timer
    timeoutId = setTimeout(() => {
      fn.apply(null, args);
    }, delay);
  };
};

form.addEventListener(
  "input",
  debounce(function (e) {
    switch (e.target.id) {
      case "first_name":
        Checkfirst_nameE1();
        break;
      case "last_name":
        Checklast_nameE1();
        break;
      case "email":
        checkEmail();
        break;
      case "password":
        checkPassword();
        break;
      case "confirm-password":
        checkConfirmPassword();
        break;
      case "contact":
        CheckContact();
        break;
      case "dob":
        Checkdob();
        break;
      case "gender":
        Checkgender();
        break;
    }
  })
);
