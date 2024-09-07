const themeButton = document.getElementById('themeButton');
let toggleTheme = true

document.addEventListener('DOMContentLoaded', (event) => {
    const darkMode = localStorage.getItem('darkMode'); 
    if (darkMode === 'enabled') {
        enableDarkMode();
    }
});

themeButton.addEventListener('click', function() {
    const darkMode = localStorage.getItem('darkMode'); 
    if (darkMode !== 'enabled') {
        enableDarkMode();
    } else { 
        disableDarkMode();
    }
});

const enableDarkMode = () => {
    themeButton.innerHTML = "<i class='bx bx-sun'></i>";
    document.documentElement.style.setProperty('--main-color', '#131314');
    document.documentElement.style.setProperty('--second-color', '#f2f2f7');
    document.documentElement.style.setProperty('--bg-color', '#131313');
    document.documentElement.style.setProperty('--shadow-color', '#0C0C0Dcc');
    localStorage.setItem('darkMode', 'enabled');
}

const disableDarkMode = () =>{ 
    themeButton.innerHTML = "<i class='bx bx-moon'></i>";
    document.documentElement.style.setProperty('--main-color', '#ffffff');
    document.documentElement.style.setProperty('--second-color', '#0C0C0D');
    document.documentElement.style.setProperty('--bg-color', '#fafafa');
    document.documentElement.style.setProperty('--shadow-color', '#0C0C0D80');
    localStorage.setItem('darkMode', 'disabled');
}

const searchBar = () => {
    const input = document.getElementById("searchBar");
    const filter = input.value.toUpperCase();
    const table = document.getElementById("table-content");
    const tr = table.getElementsByTagName("tr");

    for (let i = 1; i < tr.length; i++) {
        const td = tr[i].getElementsByTagName("td");
        let rowMatchesFilter = false;

        for (let j = 0; j < td.length; j++) {
            const txtValue = td[j].textContent || td[j].innerText;
            if (txtValue.toUpperCase().includes(filter)) {
                rowMatchesFilter = true;
                break;
            }
        }

        tr[i].style.display = rowMatchesFilter ? "" : "none";
    }
};

const interventionInput = document.getElementById('interventionInput');
const interventionList = document.getElementById('table-content');

const addIntervention = (context) => {
    if (context == "order") {
        const  interventionValue = interventionInput.value.trim();
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td><input type="text" value="${interventionValue}" name="interventionItem" required></td>
            <td class="action">
                <a onclick="deleteIntervention(this)"><i class='bx bx-trash'></i></a>
            </td>
        `;
        interventionList.append(tr)
        interventionInput.value = '';
    } else if (context == 'invoice') {
        const  interventionValue = interventionInput.value.trim();
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td><input type="text" value="${interventionValue}" name="interventionItem" required></td>
            <td><input class="quantity-input" type="number" step="any" value="0" min="0" name="QuantityValue" required></td>
            <td><input class="unit-price-input" type="number" step="any" value="0" min="0" name="UnitPriceValue" required></td>
            <td><input id="tva" type="number" value="21" name="" disabled></td>
            <td><input class="discount-input" type="number" value="0" min="0" max="100" name="DiscountValue" required></td>
            <td><input class="amount-input" type="number" value="0" step="any" value="0" name="AmountValue"></td>
            <td class="action">
                <a onclick="deleteIntervention(this)"><i class='bx bx-trash'></i></a>
            </td>
        `;
        interventionList.append(tr)
        interventionInput.value = '';
    }
}

const deleteIntervention = (intervention) => {
    const tr = intervention.closest('tr');
    tr.remove();
    calculAmount();
}

const calculAmount = () => {
    const quantityInputs = document.querySelectorAll('.quantity-input');
    const unitPriceInputs = document.querySelectorAll('.unit-price-input');
    const discountInputs = document.querySelectorAll('.discount-input');
    const amountInputs = document.querySelectorAll('.amount-input');

    console.log('render');
    let totalDiscount = 0;
    let totalHTVA = 0;
    let totalTVA = 0;
    let totalTVAC = 0;

    quantityInputs.forEach((quantityInput, index) => {
        const quantity = parseFloat(quantityInput.value);
        const unitPrice = parseFloat(unitPriceInputs[index].value);
        const discount = parseFloat(discountInputs[index].value);
        const tva = 21;

        const amountBeforeDiscount = quantity * unitPrice;
        const amount = amountBeforeDiscount * (1 - discount / 100);
        const totalAmount = amount + (amount * tva / 100);

        totalDiscount += (amountBeforeDiscount - amount) * (1 + tva / 100);
        totalHTVA += amount;
        totalTVA += amount * (tva / 100);
        totalTVAC += totalAmount;

        amountInputs[index].value = totalAmount.toFixed(2);
    });

    document.getElementById("discount-total").value = totalDiscount.toFixed(2);
    document.getElementById("discountTotal").value = totalDiscount.toFixed(2);
    document.getElementById("HTVA-total").value = totalHTVA.toFixed(2);
    document.getElementById("HTVATotal").value = totalHTVA.toFixed(2);
    document.getElementById("TVA-total").value = totalTVA.toFixed(2);
    document.getElementById("TVATotal").value = totalTVA.toFixed(2);
    document.getElementById("amount-total").value = totalTVAC.toFixed(2);
    document.getElementById("amountTotal").value = totalTVAC.toFixed(2);
}

document.getElementById("table-content").addEventListener("input", calculAmount);