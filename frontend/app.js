const BACKEND_URL = "http://127.0.0.1:8000";

document.addEventListener("DOMContentLoaded", function () {

    const form = document.getElementById("planForm");

    // If this is not the index page, do nothing.
    if (!form) {
        return;
    }

    const generateBtn = document.getElementById("generateBtn");
    const errorMessage = document.getElementById("errorMessage");
    const successMessage = document.getElementById("successMessage");


    form.addEventListener("submit", async function (event) {

        event.preventDefault();


        // Hide previous messages
        if (errorMessage) {
            errorMessage.style.display = "none";
            errorMessage.textContent = "";
        }

        if (successMessage) {
            successMessage.style.display = "none";
            successMessage.textContent = "";
        }


        // Disable button
        if (generateBtn) {
            generateBtn.disabled = true;
            generateBtn.textContent = "Generating your plan...";
        }


        // Get form values
        const username =
            document.getElementById("username").value.trim();

        const user_id =
            document.getElementById("user_id").value.trim();

        const age =
            Number(document.getElementById("age").value);

        const weight =
            Number(document.getElementById("weight").value);

        const goal =
            document.getElementById("goal").value;

        const intensity =
            document.getElementById("intensity").value;


        // Prepare data for FastAPI
        const userData = {
            username: username,
            user_id: user_id,
            age: age,
            weight: weight,
            goal: goal,
            intensity: intensity
        };


        try {

            // Connect to FastAPI
            const response = await fetch(
                `${BACKEND_URL}/generate-workout`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify(userData)
                }
            );


            // Read FastAPI response
            const result = await response.json();


            // Handle backend errors
            if (!response.ok) {
                throw new Error(
                    result.detail ||
                    "Unable to generate workout plan."
                );
            }


            // Save generated plan
            localStorage.setItem(
                "fitbuddy_result",
                JSON.stringify(result)
            );


            // Save user ID
            localStorage.setItem(
                "fitbuddy_user_id",
                user_id
            );


            // Show success message
            if (successMessage) {
                successMessage.textContent =
                    "Your 7-day fitness plan has been generated successfully!";

                successMessage.style.display = "block";
            }


            // Open FastAPI feedback page
            setTimeout(function () {

                window.location.href =
                    `${BACKEND_URL}/feedback?user_id=${encodeURIComponent(user_id)}`;

            }, 700);


        } catch (error) {

            console.error(
                "FitBuddy Error:",
                error
            );


            // Show error
            if (errorMessage) {

                errorMessage.textContent =
                    error.message ||
                    "Cannot connect to FitBuddy backend.";

                errorMessage.style.display = "block";
            }


            // Enable button again
            if (generateBtn) {

                generateBtn.disabled = false;

                generateBtn.textContent =
                    "Generate 7-Day Plan";
            }
        }

    });

});