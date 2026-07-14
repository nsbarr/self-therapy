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

    var MIN_THINK_MS = 4000;
    var MAX_THINK_MS = 5000;
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

    function revealNow(turn) {
        pending.delete(turn);
        observer.unobserve(turn);
        turn.classList.remove('thinking');
        turn.classList.add('revealed');
    }

    // Instant jumps (find-in-page, End key) can move turns entirely past the
    // viewport without ever intersecting the trigger band, so the observer
    // never fires. Sweep: anything fully above the viewport appears
    // immediately. Only what's truly behind the reader — a fast touch flick
    // sweeps scroll handlers before the observer delivers, so sweeping at the
    // reading line would skip the thinking beat for turns still on screen.
    var sweepQueued = false;
    function sweepPassedTurns() {
        sweepQueued = false;
        pending.forEach(function (turn) {
            if (turn.getBoundingClientRect().bottom < 0) {
                revealNow(turn);
            }
        });
    }
    function queueSweep() {
        if (sweepQueued) return;
        sweepQueued = true;
        requestAnimationFrame(sweepPassedTurns);
    }
    window.addEventListener('scroll', queueSweep, { passive: true });

    // Deep links land the reader mid-conversation: everything up to and
    // including the linked turn is already "read", so it appears at once.
    function revealThroughHash() {
        if (!location.hash) return;
        var target;
        try { target = document.querySelector(location.hash); } catch (err) { return; }
        if (!target) return;
        var linked = target.closest('.turn');
        if (!linked) return;
        pending.forEach(function (turn) {
            if (turn === linked || (turn.compareDocumentPosition(linked) & Node.DOCUMENT_POSITION_FOLLOWING)) {
                revealNow(turn);
            }
        });
    }
    window.addEventListener('hashchange', revealThroughHash);
    revealThroughHash();
    sweepPassedTurns();
})();
