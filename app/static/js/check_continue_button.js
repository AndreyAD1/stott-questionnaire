function administrate_continue_button() {
  var selected_sex = (male_button.checked || female_button.checked);
  if (age_form.value && selected_sex) {
    button.classList.remove("disabled");
  };
  if (!age_form.value) {
    button.classList.add("disabled");
  };
};

var age_form = document.querySelector(".form-control");
var male_button = document.querySelector('.male')
var female_button = document.querySelector('.female')
var button = document.querySelector(".continue-button");
age_form.addEventListener("change", administrate_continue_button);
male_button.addEventListener("click", administrate_continue_button);
female_button.addEventListener("click", administrate_continue_button);