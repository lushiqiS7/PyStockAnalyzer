function handleClick() {
    const input = document.getElementById('userInput');
    const output = document.getElementById('output');
    
    if (input.value.trim() === '') {
        output.innerHTML = '<p>Please enter some text first!</p>';
        output.style.color = 'red';
    } else {
        output.innerHTML = `
            <p>You entered: <strong>${input.value}</strong></p>
            <p>Length: ${input.value.length} characters</p>
        `;
        output.style.color = 'green';
    }
    
    // Clear input after submission
    input.value = '';
}

// Add event listener for Enter key
document.getElementById('userInput').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        handleClick();
    }
});