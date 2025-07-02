document.querySelectorAll('.progressbar').forEach(progressbar => {
    setTimeout(() => {
        progressbar.style.transition = 'width 8s';
        progressbar.style.width = '0%';

        setTimeout(() => {
            progressbar.parentElement.parentElement.style.display = 'none';
        }, 8000);
    }, 0);
});