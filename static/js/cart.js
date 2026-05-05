// Global Cart AJAX Handler
document.addEventListener('DOMContentLoaded', function() {
    console.log('Cart AJAX Handler initialized');

    // Helper to update Navbar Cart Count
    function updateNavbarCartCount(count) {
        let badges = document.querySelectorAll('.cart-count-badge');
        
        if (badges.length === 0 && count > 0) {
            // If badge doesn't exist but we have items, find the cart link and inject it
            const cartLinks = document.querySelectorAll('a[href*="/cart/"]');
            cartLinks.forEach(link => {
                if (link.querySelector('i.fa-shopping-bag')) {
                    const badge = document.createElement('span');
                    badge.className = 'cart-count-badge absolute -top-1.5 -right-2 bg-black text-white text-[10px] font-semibold w-4 h-4 rounded-full flex items-center justify-center';
                    badge.textContent = count;
                    link.classList.add('relative'); // Ensure parent is relative
                    link.appendChild(badge);
                }
            });
            return;
        }

        badges.forEach(badge => {
            badge.textContent = count;
            if (count > 0) {
                badge.style.display = 'flex';
            } else {
                badge.style.display = 'none';
            }
        });
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
                    // Visual feedback
                    const prevBg = submitBtn.style.backgroundColor;
                    const prevColor = submitBtn.style.color;
                    submitBtn.style.backgroundColor = '#000';
                    submitBtn.style.color = '#fff';
                    submitBtn.textContent = 'ADDED';
                    setTimeout(() => {
                        submitBtn.style.backgroundColor = prevBg;
                        submitBtn.style.color = prevColor;
                        submitBtn.innerHTML = originalBtnText;
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
        cartItemsContainer.addEventListener('click', function(e) {
            const btn = e.target.closest('button[name="action"]');
            if (btn && btn.closest('.update-qty-form')) {
                e.preventDefault();
                const form = btn.closest('.update-qty-form');
                const action = btn.value;
                const formData = new FormData(form);
                formData.append('action', action);
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
                            const row = form.closest('.cart-item-row');
                            row.style.opacity = '0';
                            setTimeout(() => {
                                row.remove();
                                if (document.querySelectorAll('.cart-item-row').length === 0) {
                                    location.reload(); // Show empty cart state
                                }
                            }, 300);
                            updateNavbarCartCount(data.cart_count);
                            return;
                        }
                        
                        const row = form.closest('.cart-item-row');
                        if (row) {
                            const qtySpan = row.querySelector('.item-qty-display');
                            const lineTotalSpans = row.querySelectorAll('.item-line-total');
                            if (qtySpan) qtySpan.textContent = data.quantity;
                            lineTotalSpans.forEach(span => span.textContent = '$' + data.line_total);
                        }
                        
                        updateNavbarCartCount(data.cart_count);
                        const subtotal = document.querySelector('#cartSubtotalDisplay');
                        const total = document.querySelector('#cartTotalDisplay');
                        if (subtotal) subtotal.textContent = '$' + data.cart_total;
                        if (total) total.textContent = '$' + data.cart_total;
                    } else {
                        alert(data.message);
                    }
                });
            }
        });

        // Handle Delete Confirmation
        cartItemsContainer.addEventListener('click', function(e) {
            const removeBtn = e.target.closest('.remove-item-btn');
            if (removeBtn) {
                e.preventDefault();
                const form = removeBtn.closest('form');
                const productName = removeBtn.dataset.productName;
                
                showDeleteModal(productName, () => {
                   const formData = new FormData(form);
                   fetch(form.action, {
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
                           const row = form.closest('.cart-item-row');
                           row.style.opacity = '0';
                           row.style.transform = 'translateX(20px)';
                           setTimeout(() => {
                               row.remove();
                               if (document.querySelectorAll('.cart-item-row').length === 0) {
                                   location.reload();
                               }
                           }, 400);
                           updateNavbarCartCount(data.cart_count);
                       }
                   });
                });
            }
        });
    }

    // Modal Logic
    function showDeleteModal(name, onConfirm) {
        const modal = document.getElementById('deleteConfirmModal');
        const nameSpan = document.getElementById('modalProductName');
        const confirmBtn = document.getElementById('confirmDeleteBtn');
        const cancelBtn = document.getElementById('cancelDeleteBtn');

        if (!modal) return;

        nameSpan.textContent = name;
        modal.classList.remove('hidden');
        modal.classList.add('flex');
        document.body.style.overflow = 'hidden';

        const closeModal = () => {
            modal.classList.add('hidden');
            modal.classList.remove('flex');
            document.body.style.overflow = '';
        };

        confirmBtn.onclick = () => {
            onConfirm();
            closeModal();
        };

        cancelBtn.onclick = closeModal;
        modal.onclick = (e) => { if(e.target === modal) closeModal(); };
    }
});
