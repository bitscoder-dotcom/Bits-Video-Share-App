// JavaScript for short videos functionality
document.addEventListener('DOMContentLoaded', function() {
    const shortVideoContainers = document.querySelectorAll('.short-video-container');
    
    shortVideoContainers.forEach(container => {
        const video = container.querySelector('.short-video');
        const actions = container.querySelector('.short-video-actions');
        
        // Play/pause on click
        container.addEventListener('click', function(e) {
            if (e.target === video) {
                if (video.paused) {
                    video.play();
                } else {
                    video.pause();
                }
            }
        });
        
        // Like button functionality
        const likeBtn = actions.querySelector('.short-video-action-btn:first-child');
        likeBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            this.classList.toggle('text-danger');
            const countSpan = this.querySelector('span');
            countSpan.textContent = this.classList.contains('text-danger') ? 
                parseInt(countSpan.textContent) + 1 : 
                parseInt(countSpan.textContent) - 1;
        });
        
        // Comment button functionality
        const commentBtn = actions.querySelector('.short-video-action-btn:nth-child(2)');
        commentBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            // In a real app, this would open a comment modal
            alert('Comment functionality would open a modal here');
        });
        
        // Share button functionality
        const shareBtn = actions.querySelector('.short-video-action-btn:last-child');
        shareBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            if (navigator.share) {
                navigator.share({
                    title: video.dataset.title,
                    text: 'Check out this short video!',
                    url: window.location.href,
                })
                .catch(err => {
                    console.log('Error sharing:', err);
                });
            } else {
                alert('Web Share API not supported in your browser');
            }
        });
    });
    
    // Handle short video scrolling
    const observer = new IntersectionObserver(
        (entries) => {
            entries.forEach(entry => {
                const video = entry.target.querySelector('.short-video');
                if (entry.isIntersecting) {
                    video.play();
                } else {
                    video.pause();
                }
            });
        },
        { threshold: 0.7 }
    );
    
    shortVideoContainers.forEach(container => {
        observer.observe(container);
    });
});
