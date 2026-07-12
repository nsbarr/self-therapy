// Progressive turn reveal. Every turn fades in when its top crosses the
// "reading line" (70% of the viewport height) — i.e. when the reader has
// actually arrived. Claude's turns hold a "thinking" beat there first, scaled
// to the length of the reply: longer answers think longer, within taste.
// Because Nick's next question shares the same trigger line, it stays hidden
// until Claude's pending reply above it has had its moment.
// Purely presentational — with JS disabled or reduced motion, the full
// conversation is simply visible.
(function () {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    if (!('IntersectionObserver' in window)) return;

    document.documentElement.classList.add('conv-animated');

    var MIN_THINK_MS = 1500;
    var MAX_THINK_MS = 3200;
    var MS_PER_WORD = 4;
    var READING_LINE = 0.7; // fraction of viewport height

    function thinkDuration(turn) {
        var body = turn.querySelector('.turn-body');
        var words = body ? body.textContent.trim().split(/\s+/).length : 0;
        return Math.min(MAX_THINK_MS, MIN_THINK_MS + words * MS_PER_WORD);
    }

    var pending = new Set();

    var observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
            if (!entry.isIntersecting) return;
            var turn = entry.target;
            observer.unobserve(turn);
            pending.delete(turn);
            if (turn.classList.contains('turn-claude')) {
                turn.classList.add('thinking');
                setTimeout(function () {
                    turn.classList.remove('thinking');
                    turn.classList.add('revealed');
                }, thinkDuration(turn));
            } else {
                turn.classList.add('revealed');
            }
        });
    }, { rootMargin: '0px 0px -' + Math.round((1 - READING_LINE) * 100) + '% 0px', threshold: 0 });

    document.querySelectorAll('.conversation .turn').forEach(function (turn) {
        pending.add(turn);
        observer.observe(turn);
    });

    // Instant jumps (deep links, find-in-page, End key) can move turns from
    // below the trigger band to above the viewport without ever intersecting
    // it, so the observer never fires. Sweep: anything fully above the reading
    // line appears immediately — the theater is only for what's ahead.
    var sweepQueued = false;
    function sweepPassedTurns() {
        sweepQueued = false;
        var lineY = window.innerHeight * READING_LINE;
        pending.forEach(function (turn) {
            if (turn.getBoundingClientRect().bottom < lineY) {
                pending.delete(turn);
                observer.unobserve(turn);
                turn.classList.remove('thinking');
                turn.classList.add('revealed');
            }
        });
    }
    function queueSweep() {
        if (sweepQueued) return;
        sweepQueued = true;
        requestAnimationFrame(sweepPassedTurns);
    }
    window.addEventListener('scroll', queueSweep, { passive: true });
    window.addEventListener('hashchange', queueSweep);
    sweepPassedTurns();
})();
