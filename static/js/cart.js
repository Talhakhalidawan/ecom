// Global Cart AJAX Handler
document.addEventListener('DOMContentLoaded', function() {
    console.log('Cart AJAX Handler initialized');

    // Helper to update Navbar Cart Count
    function updateNavbarCartCount(count) {
        const badges = document.querySelectorAll('.cart-count-badge');
        badges.forEach(badge => {
            badge.textContent = count;
            if (count > 0) {
                badge.classList.remove('hidden');
            } else {
                badge.classList.add('hidden');
            }
        });
        
        // If badge doesn't exist but count > 0, we might need more aggressive DOM manipulation
        // But for stay simple, we ensure the badge is always in HTML but hidden if 0
    }

    // Intercept Add to Cart forms
    document.addEventListener('submit', function(e) {
        if (e.target.hasAttribute('data-ajax-cart')) {
            e.preventDefault();
            const form = e.target;
            const formData = new FormData(form);
            const url = form.action;
            const submitBtn = form.querySelector('button[type="submit"]');
            const originalBtnText = submitBtn.innerHTML;

            // Simple loading state
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';

            fetch(url, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': formData.get('csrfmiddlewaretoken')
                }
            })
            .then(response => response.json())
            .then(data => {
                submitBtn.disabled = false;
                submitBtn.innerHTML = originalBtnText;

                if (data.status === 'success') {
                    updateNavbarCartCount(data.cart_count);
                    // Show success message (using alert for now, can be changed to toast)
                    // alert(data.message);
                    
                    // Optional: Visual feedback on button
                    const prevBg = submitBtn.style.backgroundColor;
                    submitBtn.style.backgroundColor = '#10b981'; // Green
                    setTimeout(() => {
                        submitBtn.style.backgroundColor = prevBg;
                    }, 2000);
                } else {
                    alert(data.message || 'Error adding to cart');
                }
            })
            .catch(error => {
                submitBtn.disabled = false;
                submitBtn.innerHTML = originalBtnText;
                console.error('Cart Error:', error);
            });
        }
    });

    // Handle Quantity Updates in Cart Page
    const cartItemsContainer = document.querySelector('#cartItemsContainer');
    if (cartItemsContainer) {
        cartItemsContainer.addEventListener('submit', function(e) {
            if (e.target.matches('.update-qty-form')) {
                e.preventDefault();
                const form = e.target;
                const formData = new FormData(form);
                formData.append('action', e.submitter.value);
                const url = form.action;

                fetch(url, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest',
                        'X-CSRFToken': formData.get('csrfmiddlewaretoken')
                    }
                })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        if (data.action === 'removed') {
                            location.reload(); // Simplest for removal
                            return;
                        }
                        
                        // Update UI
                        const row = form.closest('.cart-item-row');
                        if (row) {
                            const qtySpan = row.querySelector('.item-qty-display');
                            const lineTotalSpan = row.querySelector('.item-line-total');
                            if (qtySpan) qtySpan.textContent = data.quantity;
                            if (lineTotalSpan) lineTotalSpan.textContent = '$' + data.line_total;
                        }
                        
                        // Update totals
                        updateNavbarCartCount(data.cart_count);
                        const cartTotalSpan = document.querySelector('#cartTotalDisplay');
                        const cartSubtotalSpan = document.querySelector('#cartSubtotalDisplay');
                        if (cartTotalSpan) cartTotalSpan.textContent = '$' + data.cart_total;
                        if (cartSubtotalSpan) cartSubtotalSpan.textContent = '$' + data.cart_total;
                    } else {
                        alert(data.message);
                    }
                });
            }
        });
    }
});
