// You can fetch transaction details from an API or a database
const transactionDetails = [
    // Sample data
    { id: 1, amount: 100.00, date: '2023-11-19', description: 'Product Purchase' },
    { id: 2, amount: 50.00, date: '2023-11-20', description: 'Service Fee' },
    // Add more transactions as needed
];

const transactionContainer = document.getElementById('transaction-details');

// Function to display transaction details
function displayTransactions() {
    transactionContainer.innerHTML = '';
    transactionDetails.forEach(transaction => {
        const transactionDiv = document.createElement('div');
        transactionDiv.innerHTML = `
            <h3>Transaction ID: ${transaction.id}</h3>
            <p>Date: ${transaction.date}</p>
            <p>Amount: $${transaction.amount.toFixed(2)}</p>
            <p>Description: ${transaction.description}</p>
            <hr>
        `;
        transactionContainer.appendChild(transactionDiv);
    });
}

// Display transactions when the page loads
window.onload = displayTransactions;
