// Πρώτη Λειτουργία searchInput = document.getElementById("searchInput");

// Δεύτερη Λειτουργία

function toggleLike(button) {
    // Παίρνουμε την κάρτα προϊόντος και το όνομα του προϊόντος από τα data attributes
    const productCard = button.closest('.product-card');
    const productName = productCard.getAttribute('data-name');
    
    // Παίρνουμε το κουμπί like και το στοιχείο που εμφανίζει τον αριθμό των likes
    const likeButton = button;
    const likeCountElement = button.querySelector('.like-count');

    // Μετατρέπουμε το κείμενο του like count σε ακέραιο αριθμό
    let likeCount = parseInt(likeCountElement.textContent);

    /* Αν το κουμπί έχει ήδη την κλάση 'liked', 
    αφαιρούμε την κλάση και μειώνουμε τον αριθμό των likes, 
    αλλιώς προσθέτουμε την κλάση και αυξάνουμε τον αριθμό των likes */

    if (likeButton.classList.contains('liked')) {
        likeButton.classList.remove('liked');
        likeCount--;
    } else {
        likeButton.classList.add('liked');
        likeCount++;
    }

    // Ενημερώνουμε το κείμενο του like count με τον νέο αριθμό
    likeCountElement.textContent = likeCount;

    // Ενημέρωση του backend για την αλλαγή της κατάστασης like (ακόμη δεν είναι υλοποιημένο)

    /* try {
        const response = await fetch('http://127.0.0.1:5000/like', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ productName: productName })
        });
    } catch (error) {
        console.error('Προέκυψε κάποιο σφάλμα με το fetch των δεδομένων:');
    }*/
}

// Τρίτη Λειτουργία

async function currentSlide() {
    /*try {
        const response = await fetch('http://127.0.0.1:5000/', {
            method: 'GET',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ query: searchInput.value })
        });
        const data = await response.json();

    } catch (error) {
    console.error('Προέκυψε κάποιο σφάλμα με το fetch των δεδομένων:');
    }*/
}

// Δευτερεύουσες Λειτουργίες

function sortByLikes(){
    // Διαλέγω όλες τις κάρτςε με τους ανεμιστήρες
    const productCards = document.querySelectorAll('.product-card');

    // Ταξινομώ κατά φθίνουσα σειρά με κριτήριο το like count ανά ζεύγη (a, b)
    const sortedCards = Array.from(productCards).sort((a, b) => {
        const likesA = parseInt(a.querySelector('.like-count').textContent);
        const likesB = parseInt(b.querySelector('.like-count').textContent);
        return likesB - likesA;
    });

    products = document.getElementById('productsGrid');

    // Ενημερώνω το DOM με τις ταξινομημένες κάρτες
    sortedCards.forEach(card => {
        products.appendChild(card);
    });
}