const hideError = () => {
    const myAlert = document.getElementById('myAlert');
    if (myAlert ) {
        myAlert.classList.remove('show');
        myAlert.classList.add('d-none');
    }
}

const showError = (msg) => {
    const myAlert = document.getElementById('myAlert');
    if (myAlert) {
        myAlert.innerHTML = msg;
        myAlert.classList.remove('d-none');
        myAlert.classList.add('show');
    }
}