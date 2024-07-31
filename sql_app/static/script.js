function redirectToInstructions() {
  window.location.href = "/static/frontend/instructions.html";
}

function logout() {
  localStorage.removeItem("id")
  history.replaceState(null, "", "/static/frontend/index.html");
  location.reload()
}

function redirectTohome() {
  const emailInput = document.getElementById("email");
  const email = emailInput.value;
  if (!isValidEmail(email)) {
    emailInput.classList.add("is-invalid");
    return;
  } else {
    emailInput.classList.remove("is-invalid");
  }
  const password = document.getElementById("psw").value;

  const requestData = {
    email: email,
    password: password
  };

  fetch("http://localhost:8000/login", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(requestData)
  })
    .then(response => {
      if (!response.ok) {
        throw new Error("Error: " + response.status);
      }
      return response.json();
    })
    .then(data => {
      if(data.ch===0){
        window.location.href="http://localhost:8000/info/"+data.id
      }
      else{
      localStorage.setItem("id", data.id);
      window.location.href = "/static/frontend/home.html";
      }
    })
    .catch(error => {
      // Display error message or perform error handling
      console.error(error);
      // Show error message to the user
      alert("User details not found");
    });
}

function isValidEmail(email) {
      // Regular expression for email validation
      const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      return emailPattern.test(email);
    }

 
 function checkuser(){
    // Make the API call
    fetch("http://localhost:8000/check-user")
      .then(response => response.json())
      .then(data => {
        if (data.success === "True") {
          console.log(data)
          window.location.href = "/static/frontend/register.html";
        } else {
          // Failure, redirect to gay.html
          window.location.href = "/static/frontend/gay.html";
        }
      })
      .catch(error => {
        console.error("Error:", error);
        // Handle the error and redirect to an error page if needed
      });
  }


// script.js
document.addEventListener("DOMContentLoaded", function () {
  const registerForm = document.getElementById("register-form");
  const registerButton = document.getElementById("register-btn");

  registerForm.addEventListener("submit", function (event) {
    event.preventDefault();

    // Get form data
    const formData = new FormData(registerForm);
    const user = {
      name: formData.get("name"),
      email: formData.get("email"),
      password: formData.get("password"),
    };

    // Send the POST request to the backend API
    fetch("http://localhost:8000/register-user", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(user),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then((data) => {
        // Handle the response data here, e.g., redirect to localhost
        console.log("Registration successful:", data);
        window.location.href = "http://localhost:8000/"; // Replace with the desired destination URL
      })
      .catch((error) => {
        const temp_msg = "Registrartion failed: "+error.message;
        alert(temp_msg);
      });
  });
});


// script.js
document.addEventListener("DOMContentLoaded", function () {
  const studentForm = document.getElementById("form-pagination");

  studentForm.addEventListener("submit", function (event) {
    event.preventDefault();

    // Add this line to check if the event listener is triggered
    console.log("Form submission event triggered.");

    const nameInput = document.getElementById("name");
    const commInput = document.getElementById("community");
    const annualInput = document.getElementById("annual_income");
    const instInput = document.getElementById("inst_name");
    const courseInput = document.getElementById("course_name");
    const get_id = localStorage.getItem("id");

    const studentData = {
      name: nameInput.value,
      community: commInput.value,
      annual_income: annualInput.value,
      inst_name: instInput.value,
      course_name: courseInput.value,
      user_id: get_id,
    };
    console.log("Form Data:", studentData);
            fetch("http://localhost:8000/add-details", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(studentData),
        })
        .then((response) =>  {
          const sub_id=localStorage.getItem("id");
          window.location.href="http://localhost:8000/info/"+sub_id
        })
        .catch(error => {
          console.error("Error fetching data:", error);
        });
  });
});
