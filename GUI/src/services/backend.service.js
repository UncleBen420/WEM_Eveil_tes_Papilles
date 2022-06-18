import AxiosService from "./axios.service";

const BackendService = {
    init(url) {
        console.log(url);
        this.axiosService = new AxiosService(url);
    },

    healthCheck() {
        return this.axiosService.get('/');
    },

    recipeByIngredients(type, ingredients) {
        return this.axiosService.get('/Recipes/ByIngredients/', {
            type,
            ingredients,
        });
    },

    recipeByParam(type, duration, nbPeople, score) {
        return this.axiosService.get('/Recipes/ByParam/', {
            type,
            duration: duration.join(','),
            'nb_people': nbPeople.join(','),
            score: score.join(','),
        });
    },

    recipeSuggestion(recipe) {
        return this.axiosService.get('/Recipes/Suggestion/', {
            recipe: recipe.replace(/\s+/g, '_'),
        });
    },

    recipeReplacement(recipe, ingredients) {
        return this.axiosService.get('/Recipes/Replacement/', {
            recipe: recipe.replace(/\s+/g, '_'),
            ingredient,
        });
    },

    recipeToPredictWine(recipe) {
        return this.axiosService.get('/Wines/Pairing/', {
            recipe: recipe.replace(/\s+/g, '_'),
        });
    },

    wineToPredictRecipe(wine) {
        return this.axiosService.get('/Recipes/Pairing/', {
            wine: wine.replace(/\s+/g, '_'),
        });
    },
};

export default BackendService;
