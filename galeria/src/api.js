
import axios from "axios";

class Api {
    static get baseURL() {
        return "http://localhost:5000"
    }

    constructor() {
        this.api = axios.create({
            baseURL: Api.baseURL
        });

        this.jwt = null;
    }

    get(route) {
        return this.api.get(route, {
            headers: {
                Authorization: this.jwt ? `${this.jwt}` : "",
                Accept: "*/*"
            }
        });
    }

    post(route, data) {

        return this.api.post(route, data, {
            headers: {
                Authorization: this.jwt ? `${this.jwt}` : "",
                Accept: "*/*"
            }
        });
    }
    
    put(route, data) {
        return this.api.put(route, data, {
            headers: {
                Authorization: this.jwt ? `${this.jwt}` : "",
                Accept: "*/*"
            }
        });
    }

    delete(route) {
        return this.api.delete(route, {
            headers: {
                Authorization: this.jwt ? `${this.jwt}` : "",
                Accept: "*/*"
            }
        });
    }

    setAuthToken(jwt) {
        this.jwt = jwt;
    }

};

const api = new Api();

export default api;
