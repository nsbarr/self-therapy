// Floating waypoint for the book pages. Once the reader has scrolled past
// the contents table, a small pill names the chapter they're in and offers
// the way back to the contents. Purely presentational — with JS disabled
// the page is simply a long scroll with a contents table at the top.
(function () {
    var waypoint = document.getElementById('bookWaypoint');
    var chapterLink = document.getElementById('waypointChapter');
    var contents = document.getElementById('contents');
    if (!waypoint || !chapterLink || !contents) return;

    var chapters = Array.prototype.map.call(
        document.querySelectorAll('.book-body h1[id]'),
        function (heading) {
            var kicker = heading.querySelector('.chapter-kicker');
            var passion = heading.querySelector('.chapter-passion');
            return {
                el: heading,
                label: kicker && passion
                    ? kicker.textContent.trim() + ' · ' + passion.textContent.trim()
                    : heading.textContent.trim()
            };
        }
    );
    if (!chapters.length) return;

    var current = null;
    var ticking = false;

    function update() {
        ticking = false;
        // The chapter being read: the last opener above the top third of
        // the viewport. Below the contents table, there's always one.
        var readingLine = window.innerHeight * 0.33;
        var active = null;
        for (var i = 0; i < chapters.length; i++) {
            if (chapters[i].el.getBoundingClientRect().top <= readingLine) {
                active = chapters[i];
            } else {
                break;
            }
        }
        var pastContents = contents.getBoundingClientRect().bottom < 0;
        var show = Boolean(active) && pastContents;
        if (show && current !== active) {
            current = active;
            chapterLink.textContent = active.label;
            chapterLink.setAttribute('href', '#' + active.el.id);
        }
        waypoint.classList.toggle('visible', show);
        waypoint.setAttribute('aria-hidden', show ? 'false' : 'true');
    }

    function queueUpdate() {
        if (ticking) return;
        ticking = true;
        requestAnimationFrame(update);
    }

    window.addEventListener('scroll', queueUpdate, { passive: true });
    window.addEventListener('resize', queueUpdate, { passive: true });
    update();
})();
