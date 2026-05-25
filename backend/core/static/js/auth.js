/**
 * static/js/auth.js — Auth page enhancements (frontend-only JS).
 * Backend auth is 100% Django session-based (form POST + {% csrf_token %}).
 */
document.addEventListener('DOMContentLoaded', function() {
    // Auto-focus first empty input
    const inputs = document.querySelectorAll('.field input');
    for (const inp of inputs) {
        if (!inp.value) { inp.focus(); break; }
    }
});
