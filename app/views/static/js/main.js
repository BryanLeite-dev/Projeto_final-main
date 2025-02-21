const socket = new WebSocket('ws://localhost:8080/websocket');

socket.onmessage = function(event) {
    alert(event.data); // Exibe uma mensagem quando uma nova avaliação é adicionada
    location.reload(); // Recarrega a página para exibir as avaliações atualizadas
};

function addReviewToPage(review) {
    const reviewsContainer = document.getElementById("reviews-container");

    const reviewElement = document.createElement("div");
    reviewElement.innerHTML = `
        <p><strong>${review.usuario}:</strong> ${review.comentario}</p>
        <p>Nota: ${review.nota}</p>
    `;

    reviewsContainer.appendChild(reviewElement);
}