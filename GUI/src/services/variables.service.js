const VariablesService = {
    init(variables) {
        // setup some fields for auto-completion
        this.BACKEND_URL = undefined;

        Object.keys(variables).forEach((key) => {
            this[key] = variables[key];
        })
    },
};

export default VariablesService;
