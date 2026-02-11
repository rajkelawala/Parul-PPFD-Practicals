$(document).ready(function () {
    $("#add-item-form").on("submit", function (e) {
        e.preventDefault();
        const newItem = $("#item-input").val().trim();
        if (newItem) {
            $.ajax({
                url: "/add_item",
                type: "POST",
                contentType: "application/json",
                data: JSON.stringify({ item: newItem }),
                success: function (response) {
                    if (response.success) {
                        updateList(response.items);
                        $("#item-input").val("");
                    } else {
                        alert(response.error || "An error occurred.");
                    }
                },
                error: function () {
                    alert("Failed to communicate with the server.");
                },
            });
        } else {
            alert("Please enter an item.");
        }
    });
    function updateList(items) {
        const list = $("#item-list");
        list.empty(); // Clear existing list
        items.forEach((item) => {
            list.append(`<li>${item}</li>`);
        });
    }
});
