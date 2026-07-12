    document.addEventListener('DOMContentLoaded', function () {
        // DOM elements
        const transcript = document.getElementById('transcript');
        const toggleAutoScrollBtn = document.getElementById('toggleAutoScroll');
        const toggleLightModeBtn = document.getElementById('toggleLightMode');
        const chapterHeaders = document.querySelectorAll('.chapter-header');
        const chapterTimes = document.querySelectorAll('.chapter-time');
        const commentaryToggles = document.querySelectorAll('.commentary-toggle');

        // Variables
        let autoScrollEnabled = false;
        let youtubePlayer;
        let userCollapseOverride = {}; // Store user's collapse preference

        // Remove any unwanted icons that might be added by the CMS/framework
        document.querySelectorAll('.unwanted-icon, .chapter-plus-icon').forEach(icon => {
            if (icon) icon.remove();
        });

        // Chapter expand/collapse functionality (without affecting video)
        chapterHeaders.forEach(header => {
            header.addEventListener('click', function (e) {
                // Ignore clicks on timestamp button
                if (e.target.classList.contains('chapter-time')) return;

                const chapterId = this.getAttribute('data-chapter');
                const content = document.querySelector(`#chapter-${chapterId} .chapter-content`);

                // Store user's explicit collapse preference to override auto-expand
                userCollapseOverride[chapterId] = this.classList.contains('expanded');

                this.classList.toggle('collapsed');
                this.classList.toggle('expanded');

                if (content.classList.contains('expanded')) {
                    content.classList.remove('expanded');
                } else {
                    // Give time for animation to complete smoothly
                    setTimeout(() => {
                        content.classList.add('expanded');
                    }, 10);
                }

                e.preventDefault();
                e.stopPropagation();
            });
        });

        // Make timestamps affect video position
        chapterTimes.forEach(time => {
            time.addEventListener('click', function (e) {
                const startTime = parseInt(this.getAttribute('data-start'));
                if (youtubePlayer && youtubePlayer.seekTo) {
                    youtubePlayer.seekTo(startTime, true);
                    youtubePlayer.playVideo();
                }

                e.preventDefault();
                e.stopPropagation();
            });
        });

        // Toggle commentary for each chapter
        if (commentaryToggles.length > 0) {
            commentaryToggles.forEach(toggleBtn => {
                toggleBtn.addEventListener('click', function () {
                    const commentaryContainer = this.closest('.commentary-container');
                    const commentary = commentaryContainer.querySelector('.commentary');

                    this.classList.toggle('active');
                    commentary.classList.toggle('show-commentary');

                    if (this.classList.contains('active')) {
                        this.textContent = 'Hide Notes';
                    } else {
                        this.textContent = 'Show Notes';
                    }
                });
            });
        }

        // Toggle auto-scroll
        if (toggleAutoScrollBtn) {
            toggleAutoScrollBtn.addEventListener('click', function () {
                autoScrollEnabled = !autoScrollEnabled;
                this.classList.toggle('active');

                if (autoScrollEnabled) {
                    this.textContent = 'Disable Flow';
                } else {
                    this.textContent = 'Enable Flow';
                }
            });
        }

        // Toggle light/dark mode
        if (toggleLightModeBtn) {
            const icon = toggleLightModeBtn.querySelector('i');
            const text = toggleLightModeBtn.querySelector('span');
            
            toggleLightModeBtn.addEventListener('click', function () {
                document.body.classList.toggle('dark-mode');
                this.classList.toggle('active');

                if (document.body.classList.contains('dark-mode')) {
                    icon.className = 'fas fa-moon';
                    text.textContent = 'Dark Mode';
                } else {
                    icon.className = 'fas fa-sun';
                    text.textContent = 'Light Mode';
                }
            });
        }

        // The iframe API wants an explicit origin when enablejsapi=1; without
        // it the postMessage handshake can silently fail and the player
        // behaves erratically (state resets, dropped seeks)
        const playerFrame = document.getElementById('youtube-player');
        if (playerFrame && playerFrame.src.indexOf('origin=') === -1) {
            playerFrame.src += (playerFrame.src.indexOf('?') === -1 ? '?' : '&')
                + 'origin=' + encodeURIComponent(window.location.origin);
        }

        // YouTube API integration
        let tag = document.createElement('script');
        tag.src = "https://www.youtube.com/iframe_api";
        let firstScriptTag = document.getElementsByTagName('script')[0];
        firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

        // When YouTube API is ready
        window.onYouTubeIframeAPIReady = function () {
            youtubePlayer = new YT.Player('youtube-player', {
                events: {
                    'onReady': onPlayerReady,
                    'onStateChange': onPlayerStateChange
                }
            });
        };

        // When player is ready
        function onPlayerReady(event) {
            // Make chapter transcripts respond to clicks
            const chapterTranscripts = document.querySelectorAll('.chapter-transcript');
            chapterTranscripts.forEach(transcript => {
                transcript.addEventListener('click', function (e) {
                    // Only highlight when clicked directly, not for chapter tracking
                    if (e.target === this || e.target.closest('.chapter-transcript') === this) {
                        chapterTranscripts.forEach(t => {
                            t.classList.remove('active-chapter');
                        });
                        this.classList.add('active-chapter');
                    }
                });
            });
        }

        // Handle player state changes
        function onPlayerStateChange(event) {
            if (event.data === YT.PlayerState.PLAYING) {
                startTracking();
            } else {
                stopTracking();
            }
        }

        let trackingInterval;

        // Start tracking video time
        function startTracking() {
            stopTracking();
            trackingInterval = setInterval(() => {
                if (youtubePlayer && youtubePlayer.getCurrentTime) {
                    updateActiveChapter(youtubePlayer.getCurrentTime());
                }
            }, 1000);
        }

        // Stop tracking
        function stopTracking() {
            if (trackingInterval) {
                clearInterval(trackingInterval);
            }
        }

        // Replace the current "updateActiveChapter" function with this enhanced version
        // Add this to your existing JavaScript section

        // Replace the current "updateActiveChapter" function and related flow logic

        // Global variables for scroll control
        let lastScrollTime = 0;
        let lastScrollPosition = 0;
        let scrollUpdateInterval = 3000; // ms between major scroll updates

        function updateActiveChapter(currentTime) {
            const chapters = document.querySelectorAll('.chapter');
            const transcripts = document.querySelectorAll('.chapter-transcript');
            const headers = document.querySelectorAll('.chapter-header');

            let activeChapter = null;
            let activeTranscript = null;
            let activeHeader = null;

            chapters.forEach(chapter => {
                const transcript = chapter.querySelector('.chapter-transcript');
                const header = chapter.querySelector('.chapter-header');
                const startTime = parseInt(transcript.getAttribute('data-start'));
                const endTime = parseInt(transcript.getAttribute('data-end'));

                if (currentTime >= startTime && currentTime < endTime) {
                    activeChapter = chapter;
                    activeTranscript = transcript;
                    activeHeader = header;
                }
            });

            // Remove active class from all elements
            transcripts.forEach(t => t.classList.remove('active-chapter'));
            headers.forEach(h => h.classList.remove('active'));

            if (activeChapter && activeTranscript && activeHeader) {
                // Add active classes
                activeTranscript.classList.add('active-chapter');
                activeHeader.classList.add('active');

                const chapterId = activeHeader.getAttribute('data-chapter');
                const content = activeChapter.querySelector('.chapter-content');

                // Only expand the chapter if the user hasn't explicitly collapsed it
                if (!userCollapseOverride[chapterId] && !content.classList.contains('expanded')) {
                    activeHeader.classList.remove('collapsed');
                    activeHeader.classList.add('expanded');

                    // Give time for animation to complete smoothly
                    setTimeout(() => {
                        content.classList.add('expanded');

                        // If auto-scroll is enabled, scroll to the beginning of the newly expanded chapter
                        if (autoScrollEnabled) {
                            setTimeout(() => {
                                smoothScrollToChapter(activeChapter, activeHeader, 0);
                            }, 300);
                        }
                    }, 10);
                }

                // Enhanced auto-scroll if enabled
                if (autoScrollEnabled) {
                    handleSmartScrolling(activeChapter, activeHeader, activeTranscript, currentTime);
                }
            }
        }

        function handleSmartScrolling(activeChapter, activeHeader, activeTranscript, currentTime) {
            const now = Date.now();

            // Determine current paragraph based on time
            const paragraphs = activeChapter.querySelectorAll('.transcript-paragraph');
            if (paragraphs.length === 0) return;

            // Get chapter time information
            const startTime = parseInt(activeTranscript.getAttribute('data-start'));
            const endTime = parseInt(activeTranscript.getAttribute('data-end'));

            // Calculate how far through this chapter we are (as a percentage)
            const chapterDuration = endTime - startTime;
            const currentProgress = currentTime - startTime;
            const progressPercent = Math.min(Math.max(currentProgress / chapterDuration, 0), 1);

            // Only scroll if enough time has passed since the last scroll
            // or if we've just changed chapters (indicated by a large change in progress)
            if (now - lastScrollTime > scrollUpdateInterval ||
                Math.abs(lastScrollPosition - progressPercent) > 0.15) {

                // Choose which paragraph to scroll to based on progress
                const targetIndex = Math.floor(progressPercent * paragraphs.length);
                const targetParagraph = targetIndex < paragraphs.length ?
                    paragraphs[targetIndex] :
                    paragraphs[paragraphs.length - 1];

                if (targetParagraph) {
                    // Scroll to the paragraph with the optimal viewing position
                    const windowHeight = window.innerHeight;
                    const headerHeight = activeHeader.offsetHeight;
                    const scrollTop = activeChapter.offsetTop + headerHeight +
                        targetParagraph.offsetTop - (windowHeight * 0.3);

                    // Scroll with gentle easing
                    window.scrollTo({
                        top: scrollTop,
                        behavior: 'smooth'
                    });

                    // Update tracking variables
                    lastScrollTime = now;
                    lastScrollPosition = progressPercent;
                }
            }
        }

        // Helper function for smooth scrolling to the beginning of a chapter
        function smoothScrollToChapter(chapter, header, delay) {
            setTimeout(() => {
                const scrollTop = chapter.offsetTop + header.offsetHeight - (window.innerHeight * 0.3);
                window.scrollTo({
                    top: scrollTop,
                    behavior: 'smooth'
                });
            }, delay);
        }

        // When setting up the player and tracking
        function startTracking() {
            stopTracking();

            // Reset scroll tracking variables
            lastScrollTime = 0;
            lastScrollPosition = 0;

            // Use a less frequent interval to check video time (every 1s instead of faster)
            trackingInterval = setInterval(() => {
                if (youtubePlayer && youtubePlayer.getCurrentTime) {
                    updateActiveChapter(youtubePlayer.getCurrentTime());
                }
            }, 1000);
        }

        // Add a more advanced flow mode option
        function enhanceFlowControls() {
            // Create a new flow speed control
            const flowControls = document.createElement('div');
            flowControls.className = 'flow-speed-controls';
            flowControls.style.display = 'none';
            flowControls.innerHTML = `
        <span class="flow-speed-label">Reading Speed:</span>
        <button class="flow-speed-btn" data-speed="0.8">Slower</button>
        <button class="flow-speed-btn active" data-speed="1">Normal</button>
        <button class="flow-speed-btn" data-speed="1.2">Faster</button>
    `;

            // Add the controls after the existing control buttons
            const controlButtons = document.querySelector('.control-buttons');
            controlButtons.parentNode.insertBefore(flowControls, controlButtons.nextSibling);

            // Flow-control styling lives in video.css

            // Update the toggle auto-scroll function
            const toggleAutoScrollBtn = document.getElementById('toggleAutoScroll');
            let flowSpeedMultiplier = 1;

            // Show/hide flow speed controls
            if (toggleAutoScrollBtn) {
                const originalClickHandler = toggleAutoScrollBtn.onclick;
                toggleAutoScrollBtn.onclick = function () {
                    autoScrollEnabled = !autoScrollEnabled;
                    this.classList.toggle('active');

                    if (autoScrollEnabled) {
                        this.textContent = 'Disable Flow';
                        flowControls.style.display = 'flex';
                    } else {
                        this.textContent = 'Enable Flow';
                        flowControls.style.display = 'none';
                    }
                };
            }

            // Add event listeners to speed buttons
            document.querySelectorAll('.flow-speed-btn').forEach(btn => {
                btn.addEventListener('click', function () {
                    document.querySelectorAll('.flow-speed-btn').forEach(b => b.classList.remove('active'));
                    this.classList.add('active');
                    flowSpeedMultiplier = parseFloat(this.getAttribute('data-speed'));
                });
            });
        }

        // Call this function when the document is loaded
        document.addEventListener('DOMContentLoaded', function () {
            // ... your existing code ...

            // Add enhanced flow controls
            enhanceFlowControls();
        });
    });
