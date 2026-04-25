/* Admin Loading Spinner Logic */
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('asset_form');
    if (form) {
        form.addEventListener('submit', function(e) {
            // Find all submit buttons (Save, Save and continue, etc.)
            const submitButtons = form.querySelectorAll('button[type="submit"], input[type="submit"]');
            
            // Check if it's a valid form before showing loading (standard HTML5 validation)
            if (form.checkValidity()) {
                submitButtons.forEach(btn => {
                    // Prevent multiple clicks
                    btn.style.pointerEvents = 'none';
                    btn.style.opacity = '0.7';
                    
                    // Add spinner icon if it's the main button
                    if (btn.classList.contains('bg-primary-600') || btn.name === '_save') {
                        const originalText = btn.innerHTML;
                        btn.innerHTML = `
                            <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white inline-block" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                            </svg>
                            Uploading...
                        `;
                    }
                });
            }
        });
    }
});
