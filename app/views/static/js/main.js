const socket = new WebSocket('ws://localhost:8080/websocket');

socket.onmessage = function(event) {
    const data = JSON.parse(event.data);

    if (data.type === "new_review") {
        const review = data.data;
        addReviewToPage(review);
    }
};

function addReviewToPage(review) {
    const reviewsContainer = document.getElementById("reviews-container");

    const reviewElement = document.createElement("div");
    reviewElement.innerHTML = `
        <strong>${review.usuario}:</strong> ${review.comentario} (Nota: ${review.nota})
    `;

    reviewsContainer.appendChild(reviewElement);
}