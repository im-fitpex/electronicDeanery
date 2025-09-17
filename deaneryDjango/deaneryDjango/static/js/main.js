// Minimal JS: close alerts, simple enhancements (no Bootstrap)
(function () {
	'use strict';

	// Close alerts when clicking .btn-close inside .alert
	document.addEventListener('click', function (e) {
		const btn = e.target.closest('.btn-close');
		if (!btn) return;
		const alert = btn.closest('.alert');
		if (alert) {
			alert.style.transition = 'opacity 200ms ease, transform 200ms ease';
			alert.style.opacity = '0';
			alert.style.transform = 'translateY(-6px)';
			setTimeout(() => alert.remove(), 220);
		}
	});

})();

