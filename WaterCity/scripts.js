const input = document.getElementById("assistantInput");
const response = document.getElementById("botResponse");
// const bookBtn = document.getElementsByClassName("book-btn")[0];
const booBtn = document.getElementById("bookBtn")

input.addEventListener("keydown", function(event) {
    if (event.key === "Enter") {
        const userMessage = input.value.trim().toLowerCase();

        if (userMessage === "hi" || userMessage === "hello") {
            response.textContent = "Hello! How can I help you today?";
        } else if (userMessage.includes("ticket")) {
            response.textContent = "You can book your tickets by clicking the  button below.";
        } else {
            response.textContent = "I'm not sure I understand that. Try saying 'hi'!";
        }

        input.value = "";
    }
});


bookBtn.addEventListener("click", function() {
    response.textContent= "🎉 Congrats! Your tickets are booked!";
})