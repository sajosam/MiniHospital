const first_nameE1 = document.querySelector("#first_name");
const last_nameE1 = document.querySelector("#last_name");
const emailEl = document.querySelector("#email");
const passwordEl = document.querySelector("#password");
const confirmPasswordEl = document.querySelector("#confirm_password");
const contactEl = document.querySelector("#contact");
const genderEl = document.querySelector("#gender");
const dobEl = document.querySelector("#dob");

const form = document.querySelector("#signup");

const Checkfirst_nameE1 = () => {
  let valid = false;
  const first_name = first_nameE1.value.trim();
  if (!isRequired(first_name)) {
    setErrorFor(first_nameE1, "First name is required");
  } else if (!isLength(first_name, 3)) {
    setErrorFor(first_nameE1, "First name must be at least 3 characters");
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
    setErrorFor(last_nameE1, "Last name is required");
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
    showError(emailEl, "Email cannot be blank.");
  } else if (!isEmailValid(email)) {
    showError(emailEl, "Email is not valid.");
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
    showError(passwordEl, "Password cannot be blank.");
  } else if (!isPasswordSecure(password)) {
    showError(
      passwordEl,
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
    showError(confirmPasswordEl, "Please enter the password again");
  } else if (password !== confirmPassword) {
    showError(confirmPasswordEl, "The password does not match");
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
    showError(contactEl, "Contact cannot be blank");
  } else if (!isContactValid(contact)) {
    showError(contactEl, "Contact is not valid");
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
    showError(genderEl, "Gender cannot be blank");
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
    showError(dobEl, "DOB cannot be blank");
  } else {
    showSuccess(dobEl);
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
    isLastNameValid = Checklast_nameE1();

  let isFormValid =
    isEmailValid &&
    isPasswordValid &&
    isConfirmPasswordValid &&
    isContactValid &&
    isGenderValid &&
    isDobValid &&
    isFirstNameValid &&
    isLastNameValid;

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
