function setupModal(inputID, modalID, calculateButtonID, value1InputID, value2InputID) {
    const inputElem = document.getElementById(inputID);
    const modalElem = document.getElementById(modalID);
    const calculateButton = document.getElementById(calculateButtonID);
    const value1Input = document.getElementById(value1InputID);
    const value2Input = document.getElementById(value2InputID);

    inputElem.addEventListener('click', function() {
        modalElem.style.display = 'block';
    });

    calculateButton.addEventListener('click', function() {
        let value1 = parseFloat(value1Input.value);
        let value2 = parseFloat(value2Input.value);

        if (!isNaN(value1) && !isNaN(value2) && value2 !== 0) {
            let resultValue = (value1 / value2) * 100;
            inputElem.value = resultValue.toFixed(2);
            modalElem.style.display = 'none';
        } else {
            alert('Please enter valid values.');
        }
    });
}

setupModal('dti', 'dtiModal', 'calculateDTI', 'debt', 'income');

// Close the modal when clicked outside
window.onclick = function(event) {
    const modalsIds = ['dtiModal', 'revolUtilModal', 'bcUtilModal'];
    if (modalsIds.includes(event.target.id)) {
        event.target.style.display = 'none';
    }
};

// Submit form and display result
document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("main_form");
    form.addEventListener("submit", function(event) {
        event.preventDefault();

        const formData = new FormData(form);
        fetch('/submit', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById("result_container").innerHTML = data.result;
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    });
});
