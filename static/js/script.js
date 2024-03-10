
function deleteProduct(productId) {
    fetch('/delete_product/' + productId, {
        method: 'DELETE',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
        },
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);

        if (data.status === 'success') {

            const row = document.getElementById(`order_item_${productId}`);
            if (row) {
                row.remove();
            }
            window.location.reload();
        } else {
            console.error('Eroare la ștergerea produsului:', data.message);
        }
    })
    .catch(error => {
        console.error('Eroare la comunicarea cu serverul:', error);
    });
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}