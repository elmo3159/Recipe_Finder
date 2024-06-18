console.log("JavaScript file loaded");

document.addEventListener('DOMContentLoaded', function () {
    console.log("DOMContentLoaded event fired");
    const ingredientInput = document.getElementById('ingredient-input');
    const autocompleteResults = document.getElementById('autocomplete-results');
    const addIngredientButton = document.getElementById('add-ingredient');
    const ingredientBox = document.getElementById('ingredient-box');
    const searchRecipesButton = document.getElementById('search-recipes');

    if (ingredientInput) {
        console.log("Ingredient input field found");
        ingredientInput.addEventListener('input', function () {
            const query = ingredientInput.value;
            console.log("Input event triggered, query:", query);
            if (query.length > 0) {
                fetch(`/search_ingredients/?query=${query}`)
                    .then(response => {
                        console.log("Fetch response received");
                        return response.json();
                    })
                    .then(data => {
                        autocompleteResults.innerHTML = '';
                        data.forEach(ingredient => {
                            const div = document.createElement('div');
                            div.textContent = ingredient.name;
                            div.dataset.id = ingredient.id;
                            div.addEventListener('click', () => {
                                addIngredientToBox(ingredient.name);
                                ingredientInput.value = '';
                                autocompleteResults.innerHTML = '';
                            });
                            autocompleteResults.appendChild(div);
                        });
                    })
                    .catch(error => console.error('Error:', error));
            } else {
                autocompleteResults.innerHTML = '';
            }
        });
    } else {
        console.log("Ingredient input field not found");
    }

    if (addIngredientButton) {
        console.log("Add ingredient button found");
        addIngredientButton.addEventListener('click', function () {
            if (ingredientInput) {
                const ingredientName = ingredientInput.value;
                console.log("Add ingredient button clicked, ingredient:", ingredientName);
                if (ingredientName) {
                    addIngredientToBox(ingredientName);
                    ingredientInput.value = '';
                    autocompleteResults.innerHTML = '';
                }
            }
        });
    } else {
        console.log("Add ingredient button not found");
    }

    function addIngredientToBox(name) {
        const li = document.createElement('li');
        li.textContent = name;
        ingredientBox.appendChild(li);
    }

    if (searchRecipesButton) {
        console.log("Search recipes button found");
        searchRecipesButton.addEventListener('click', function () {
            const ingredients = [];
            if (ingredientBox) {
                ingredientBox.querySelectorAll('li').forEach(li => ingredients.push(li.textContent));
                console.log("Search recipes button clicked, ingredients:", ingredients);
                fetch('/search_recipes/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                    },
                    body: JSON.stringify({ ingredients })
                })
                    .then(response => response.json())
                    .then(data => {
                        displayRecipes(data.recipes);
                    });
            }
        });
    } else {
        console.log("Search recipes button not found");
    }

    function displayRecipes(recipes) {
        const recipeResults = document.getElementById('recipe-results');
        const recipeList = document.getElementById('recipe-list');
        if (recipeList && recipeResults) {
            recipeList.innerHTML = '';
            recipes.forEach(recipe => {
                const li = document.createElement('li');
                const a = document.createElement('a');
                a.href = recipe.url;
                a.textContent = recipe.title;
                li.appendChild(a);
                recipeList.appendChild(li);
            });
            recipeResults.style.display = 'block';
        }
    }
});
