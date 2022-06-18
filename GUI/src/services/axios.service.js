import Axios from 'axios';

class AxiosService {
    constructor(url) {
        this.axios = Axios.create({
            headers: { 'Content-Type': 'application/json' },
            baseURL: url,
        });
    }

    async get(path, query = null) {
        return this.axios.get(path + this.toQueryString(query));
    }

    async post(path, body = {}, query) {
        return this.axios.post(path + this.toQueryString(query), body);
    }

    async put(path, body = {}) {
        return this.axios.put(path, body);
    }

    async delete(path) {
        return this.axios.delete(path);
    }

    toQueryString(query) {
        let queryString = '';
        if (query && query instanceof Object) {
            Object.entries(query).forEach(([key, value], index) => {
                queryString += index > 0 ? '&' : '?';
                queryString += `${key}=${value}`;
            });
        }
        return queryString;
    }
}

export default AxiosService;
