import AxiosService from "./axios.service";

const BackendService = {
    init(url) {
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
        const query = {type};
        let str = this.minMaxToString(duration);
        if (str != null) query.duration = str;

        str = this.minMaxToString(nbPeople);
        if (str != null) query.nb_people = str;

        str = this.minMaxToString(score);
        if (str != null) query.score = str;

        return this.axiosService.get('/Recipes/ByParam/', query);
    },
    minMaxToString(minMax) {
        if (minMax.filter((v) => v != null && v !== '').length !== 2) return null;
        return minMax.join(',');
    },

    recipeSuggestion(recipe) {
        return this.axiosService.get('/Recipes/Suggestion/', {
            recipe: recipe.replace(/\s+/g, '_'),
        });
    },

    recipeReplacement(recipe, ingredient) {
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
