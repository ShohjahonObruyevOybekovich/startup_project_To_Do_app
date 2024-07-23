// script.js
window.addEventListener('scroll', function() {
    const ad = document.getElementById('ad');
    const scrollHeight = document.documentElement.scrollHeight;
    const scrollTop = document.documentElement.scrollTop;
    const clientHeight = document.documentElement.clientHeight;

    // Show ad when the user scrolls past half of the page
    if (scrollTop + clientHeight > scrollHeight / 2) {
        ad.style.display = 'block';
    } else {
        ad.style.display = 'none';
    }
});
