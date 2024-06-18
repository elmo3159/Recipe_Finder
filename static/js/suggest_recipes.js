document.addEventListener("DOMContentLoaded", function() {
    const addIngredientButton = document.getElementById("add-ingredient");
    const searchRecipesButton = document.getElementById("search-recipes");
    const ingredientInput = document.getElementById("ingredient-input");
    const ingredientBox = document.getElementById("ingredient-box");

    addIngredientButton.addEventListener("click", function() {
        const ingredientName = ingredientInput.value.trim();
        if (ingredientName) {
            fetch("/add_ingredient/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value
                },
                body: JSON.stringify({ name: ingredientName })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const listItem = document.createElement("li");
                    listItem.textContent = data.ingredient.name;
                    ingredientBox.appendChild(listItem);
                    ingredientInput.value = "";
                }
            });
        }
    });

    searchRecipesButton.addEventListener("click", function() {
        const ingredientIds = [];
        ingredientBox.querySelectorAll("li").forEach(item => {
            ingredientIds.push(item.getAttribute("data-id"));
        });

        if (ingredientIds.length > 0) {
            fetch("/search_recipes/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value
                },
                body: JSON.stringify({ ids: ingredientIds })
            })
            .then(response => response.json())
            .then(data => {
                const recipeResults = document.getElementById("recipe-results");
                const recipeList = document.getElementById("recipe-list");
                recipeList.innerHTML = "";

                if (data.recipes.length > 0) {
                    data.recipes.forEach(recipe => {
                        const listItem = document.createElement("li");
                        const link = document.createElement("a");
                        link.href = recipe.url;
                        link.textContent = recipe.title;
                        listItem.appendChild(link);
                        recipeList.appendChild(listItem);
                    });
                    recipeResults.style.display = "block";
                } else {
                    recipeResults.style.display = "none";
                }
            });
        }
    });
});
