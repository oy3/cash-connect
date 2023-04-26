const hideError = () => {
    const myAlert = document.getElementById('myAlert');
    if (myAlert) {
        myAlert.classList.remove('show');
        myAlert.classList.add('hide');
    }
}

const showError = (msg, error) => {
    const myAlert = document.getElementById('myAlert');
    const mssg = document.getElementById('feedback-msg');

    if (myAlert) {
        if (error) {
            const toast = bootstrap.Toast.getOrCreateInstance(myAlert);
            mssg.innerHTML = msg;
            myAlert.classList.add('text-bg-danger');
            myAlert.classList.remove('text-bg-success');
            toast.show();
        }
    }
}