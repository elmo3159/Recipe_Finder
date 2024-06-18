document.addEventListener('DOMContentLoaded', function () {
    const ingredientInput = document.getElementById('ingredient-input');
    const ingredientBox = document.getElementById('ingredient-box');
    const deleteIngredientButton = document.getElementById('delete-ingredient');
    const deselectIngredientButton = document.getElementById('deselect-ingredient');
    const searchRecipesButton = document.getElementById('search-recipes');
    const autocompleteResults = document.getElementById('autocomplete-results');

    function getCSRFToken() {
        let csrfToken = null;
        const cookies = document.cookie.split(';');
        cookies.forEach(cookie => {
            const [name, value] = cookie.trim().split('=');
            if (name === 'csrftoken') {
                csrfToken = value;
            }
        });
        return csrfToken;
    }

    if (ingredientInput) {
        ingredientInput.addEventListener('input', function () {
            const query = ingredientInput.value;
            if (query.length > 0) {
                fetch(`/search_ingredients/?query=${query}`)
                    .then(response => response.json())
                    .then(data => {
                        if (autocompleteResults) {
                            autocompleteResults.innerHTML = '';
                            data.forEach(ingredient => {
                                const div = document.createElement('div');
                                div.textContent = ingredient.name;
                                div.dataset.id = ingredient.id;
                                div.addEventListener('click', () => {
                                    addIngredientToBox(ingredient.name, ingredient.id);
                                    ingredientInput.value = '';
                                    autocompleteResults.innerHTML = '';
                                });
                                autocompleteResults.appendChild(div);
                            });
                        }
                    })
                    .catch(error => {
                        console.error('Error:', error);
                    });
                } else {
                    if (autocompleteResults) {
                        autocompleteResults.innerHTML = '';
                    }
                }
            });
        }
    
        function addIngredientToBox(name, id) {
            if (ingredientBox) {
                const li = document.createElement('li');
                li.className = 'ingredient-item';
                const wrapper = document.createElement('div');
                wrapper.className = 'ingredient-wrapper';
    
                const checkbox = document.createElement('input');
                checkbox.type = 'checkbox';
                checkbox.className = 'ingredient-checkbox';
    
                const divider = document.createElement('span');
                divider.className = 'ingredient-divider';
    
                const ingredientName = document.createElement('span');
                ingredientName.className = 'ingredient-name';
                ingredientName.textContent = name;
    
                wrapper.appendChild(checkbox);
                wrapper.appendChild(divider);
                wrapper.appendChild(ingredientName);
                li.appendChild(wrapper);
    
                li.dataset.id = id !== null ? id : name;
                ingredientBox.appendChild(li);
    
                fetch('/add_ingredient/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCSRFToken()
                    },
                    body: JSON.stringify({ name: name })
                })
                    .then(response => response.json())
                    .then(data => {
                        if (!data.success) {
                            alert('Failed to add the ingredient.');
                        }
                    })
                    .catch(error => {
                        console.error('Error:', error);
                    });
            } else {
                console.error('Error: ingredientBox is null');
            }
        }
    
        if (deleteIngredientButton) {
            deleteIngredientButton.addEventListener('click', function () {
                const selectedIds = [];
                if (ingredientBox) {
                    ingredientBox.querySelectorAll('.ingredient-checkbox:checked').forEach(checkbox => {
                        const li = checkbox.closest('li');
                        selectedIds.push(li.dataset.id);
                        ingredientBox.removeChild(li);
                    });
    
                    if (selectedIds.length > 0) {
                        fetch('/delete_ingredient/', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                                'X-CSRFToken': getCSRFToken()
                            },
                            body: JSON.stringify({ ids: selectedIds })
                        })
                            .then(response => response.json())
                            .then(data => {
                                if (!data.success) {
                                    alert('Failed to delete some ingredients.');
                                }
                            });
                    }
                } else {
                    console.error('Error: ingredientBox is null');
                }
            });
        }

        if (deselectIngredientButton) {
            deselectIngredientButton.addEventListener('click', function () {
                if (ingredientBox) {
                    ingredientBox.querySelectorAll('.ingredient-checkbox:checked').forEach(checkbox => {
                        checkbox.checked = false;
                    });
                } else {
                    console.error('Error: ingredientBox is null');
                }
            });
        }
    
        if (searchRecipesButton) {
            searchRecipesButton.addEventListener('click', function () {
                const ingredients = [];
                if (ingredientBox) {
                    ingredientBox.querySelectorAll('li').forEach(li => {
                        if (li.querySelector('.ingredient-checkbox').checked) {
                            ingredients.push(li.textContent.trim());
                        }
                    });
                    if (ingredients.length === 0) {
                        ingredientBox.querySelectorAll('li').forEach(li => {
                            ingredients.push(li.textContent.trim());
                        });
                    }
                    fetch('/search_recipes/', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': getCSRFToken()
                        },
                        body: JSON.stringify({ ingredients })
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.recipes.length > 0) {
                            const form = document.createElement('form');
                            form.method = 'POST';
                            form.action = '/search_results/';
                            form.style.display = 'none';
                            const csrfInput = document.createElement('input');
                            csrfInput.name = 'csrfmiddlewaretoken';
                            csrfInput.value = getCSRFToken();
                            form.appendChild(csrfInput);
                            const dataInput = document.createElement('input');
                            dataInput.name = 'recipes';
                            dataInput.value = JSON.stringify(data.recipes);
                            form.appendChild(dataInput);
                            document.body.appendChild(form);
                            form.submit();
                        } else {
                            alert('No matching recipes found.');
                        }
                    })
                    .catch(error => {
                        console.error('Error:', error);
                    });
                } else {
                    console.error('Error: ingredientBox is null');
                }
            });
        }
    });
