/**
 * Wishlist AJAX System
 * Handles Add/Remove functionality across the site without page reloads.
 */
document.addEventListener('DOMContentLoaded', function() {
    console.log('Wishlist System Initialized');

    // 1. Unified Submit Handler for Adding to Wishlist
    document.addEventListener('submit', function(e) {
        const form = e.target;
        if (!form.hasAttribute('data-ajax-wishlist')) return;

        e.preventDefault();
        const formData = new FormData(form);
        const url = form.getAttribute('action');
        const submitBtn = form.querySelector('button[type="submit"]');
        const heartIcon = submitBtn ? submitBtn.querySelector('i.fa-heart') : null;
        
        if (submitBtn) submitBtn.disabled = true;

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
            if (submitBtn) submitBtn.disabled = false;
            
            if (data.status === 'success') {
                const action = data.action; // 'added' or 'removed'
                
                // Toggle Heart Icon and Button Classes
                if (heartIcon) {
                    if (action === 'added') {
                        heartIcon.classList.remove('far');
                        heartIcon.classList.add('fas');
                        submitBtn.classList.remove('text-gray-400', 'text-gray-500');
                        submitBtn.classList.add('text-red-500');
                    } else {
                        heartIcon.classList.remove('fas');
                        heartIcon.classList.add('far');
                        submitBtn.classList.remove('text-red-500');
                        submitBtn.classList.add('text-gray-500');
                    }
                    
                    // Subtle scale animation
                    heartIcon.style.transform = 'scale(1.3)';
                    setTimeout(() => heartIcon.style.transform = 'scale(1)', 200);
                }
                
                // Update text if it's the detail page button
                const btnText = submitBtn ? submitBtn.querySelector('span') : null;
                if (btnText) {
                    if (action === 'added') {
                        btnText.textContent = 'IN WISHLIST';
                    } else {
                        btnText.textContent = 'ADD TO WISHLIST';
                    }
                }
            } else {
                alert(data.message || 'Error updating wishlist');
                if (submitBtn) submitBtn.disabled = false;
            }
        })
        .catch(error => {
            if (submitBtn) submitBtn.disabled = false;
            console.error('Wishlist Error:', error);
        });
    });

    // 2. Handle Wishlist Page Removals (using the same toggle logic)
    const wishlistContainer = document.querySelector('#wishlistContainer');
    if (wishlistContainer) {
        wishlistContainer.addEventListener('submit', function(e) {
            const form = e.target;
            if (!form.classList.contains('remove-wishlist-from-page-form')) return;

            e.preventDefault();
            const row = form.closest('.wishlist-item-row');
            const formData = new FormData(form);

            if (row) {
                row.style.opacity = '0.5';
                row.style.pointerEvents = 'none';
            }
            
            fetch(form.getAttribute('action'), {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': formData.get('csrfmiddlewaretoken')
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success' && data.action === 'removed') {
                    if (row) {
                        row.style.opacity = '0';
                        row.style.transform = 'scale(0.95)';
                        setTimeout(() => {
                            row.remove();
                            if (document.querySelectorAll('.wishlist-item-row').length === 0) location.reload();
                        }, 400);
                    }
                } else {
                    if (row) {
                        row.style.opacity = '1';
                        row.style.pointerEvents = 'auto';
                    }
                    if (data.status !== 'success') alert(data.message || 'Error updating wishlist');
                }
            })
            .catch(error => {
                if (row) {
                    row.style.opacity = '1';
                    row.style.pointerEvents = 'auto';
                }
                console.error('Wishlist Error:', error);
            });
        });
    }
});
