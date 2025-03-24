document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("expense-form");
    const expenseList = document.getElementById("expense-list");
    const totalAmount = document.getElementById("total-amount");

    let expenses = [];

    // Add Expense Function
    form.addEventListener("submit", function (event) {
        event.preventDefault();

        let amount = parseFloat(document.getElementById("amount").value);
        let category = document.getElementById("category").value;
        let date = document.getElementById("date").value;
        let description = document.getElementById("description").value;

        if (amount && category && date) {
            let expense = { amount, category, date, description };
            expenses.push(expense);
            updateExpenseList();
        }

        form.reset();
    });

    // Update Expense List
    function updateExpenseList() {
        expenseList.innerHTML = "";
        let total = 0;

        expenses.forEach((expense, index) => {
            total += expense.amount;
            let li = document.createElement("li");
            li.innerHTML = `${expense.category} - ₹${expense.amount} <span>(${expense.date})</span>`;
            expenseList.appendChild(li);
        });

        totalAmount.innerText = total.toFixed(2);
    }
});