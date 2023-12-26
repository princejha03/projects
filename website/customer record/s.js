document.addEventListener("DOMContentLoaded", function() {
    // Sample customer records
    const customers = [
        { name: "John Doe", email: "john@example.com", phone: "555-1234", amount: "$100.00" },
        { name: "Jane Smith", email: "jane@example.com", phone: "555-5678", amount: "$150.00" },
        // Add more customer records as needed
    ];

    // Display customer records in the table
    const customerTable = document.getElementById("customer-list");

    customers.forEach(customer => {
        const row = customerTable.insertRow();
        row.insertCell(0).textContent = customer.name;
        row.insertCell(1).textContent = customer.email;
        row.insertCell(2).textContent = customer.phone;
        row.insertCell(3).textContent = customer.amount;
    });
});
