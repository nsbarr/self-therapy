// Progressive turn reveal: each turn fades in as it enters the viewport,
// with a brief "thinking" beat before Claude's turns. Purely presentational —
// with JS disabled or reduced motion, the full conversation is simply visible.
(function () {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    if (!('IntersectionObserver' in window)) return;

    document.documentElement.classList.add('conv-animated');

    var observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
            if (!entry.isIntersecting) return;
            var turn = entry.target;
            observer.unobserve(turn);
            if (turn.classList.contains('turn-claude')) {
                turn.classList.add('thinking');
                setTimeout(function () {
                    turn.classList.remove('thinking');
                    turn.classList.add('revealed');
                }, 700);
            } else {
                turn.classList.add('revealed');
            }
        });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.02 });

    document.querySelectorAll('.conversation .turn').forEach(function (turn) {
        observer.observe(turn);
    });
})();
