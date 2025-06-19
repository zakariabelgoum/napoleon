document.getElementById('searchBtn').addEventListener('click', function () {
    const searchQuery = document.getElementById('search').value;

    if (searchQuery) {
        fetchProductData(searchQuery);
    } else {
        alert('Please enter a product to search.');
    }
});

function fetchProductData(query) {
    // Example product data
    const exampleProducts = [
        {
            title: "Venum Challenger Mouthguard",
            image: "https://example.com/images/venum-mouthguard.jpg",
            price: "15.99",
            location: "USA",
            extraFees: "5.00"
        },
        {
            title: "Adidas Headgear Pro",
            image: "https://example.com/images/adidas-headgear.jpg",
            price: "29.99",
            location: "Germany",
            extraFees: "7.50"
        },
        {
            title: "Everlast Boxing Gloves",
            image: "https://example.com/images/everlast-gloves.jpg",
            price: "49.99",
            location: "UK",
            extraFees: "10.00"
        },
        {
            title: "Nike Running Shoes",
            image: "https://example.com/images/nike-shoes.jpg",
            price: "89.99",
            location: "Canada",
            extraFees: "12.00"
        },
        {
            title: "Under Armour Compression Shirt",
            image: "https://example.com/images/under-armour-shirt.jpg",
            price: "25.00",
            location: "France",
            extraFees: "4.00"
        },
    ];

    // Filter the example products based on the search query
    const filteredProducts = exampleProducts.filter(product =>
        product.title.toLowerCase().includes(query.toLowerCase())
    );

    const productList = document.getElementById('product-list');
    productList.innerHTML = '';

    // Display the filtered products in the UI
    filteredProducts.forEach(product => {
        const productRow = createProductRow(product);
        productList.appendChild(productRow);
    });
}

function createProductRow(product) {
    const productRow = document.createElement('tr');

    productRow.innerHTML = `
        <td>${product.title}</td>
        <td><img src="${product.image}" alt="${product.title}" style="width: 50px;"></td>
        <td>$${product.price}</td>
        <td>${product.location}</td>
        <td>$${product.extraFees}</td>
    `;

    return productRow;
}
