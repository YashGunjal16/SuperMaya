import axios from 'axios';

const API = axios.create({
    baseURL: 'http://localhost:8000',
});

// THIS IS THE GUARANTEED FIX.
// This interceptor runs BEFORE every single API request is sent.
API.interceptors.request.use(
    (config) => {
        // 1. Read the token from localStorage on every request.
        const token = localStorage.getItem('supermaya_token');
        
        console.log("API Interceptor: Checking for token...");

        // 2. If the token exists, attach it to the Authorization header.
        if (token) {
            config.headers['Authorization'] = `Bearer ${token}`;
            console.log("API Interceptor: Token found and attached.");
        } else {
            console.log("API Interceptor: No token found in localStorage.");
        }
        
        return config;
    },
    (error) => {
        // This handles errors in creating the request itself.
        console.error("API Interceptor Request Error:", error);
        return Promise.reject(error);
    }
);

// This interceptor helps debug responses from the server.
API.interceptors.response.use(
    (response) => response,
    (error) => {
        console.error("API Response Error:", error.response);
        return Promise.reject(error);
    }
);


// --- API Functions ---

export const login = (email, password) => {
    const formData = new FormData();
    formData.append('username', email);
    formData.append('password', password);
    return API.post('/auth/token', formData);
};

export const register = (email, password) => API.post('/auth/register', { email, password });

export const postTextQuery = (query) => API.post('/chat/text', { user_query: query });

export const postImageQuery = (query, image) => {
    const formData = new FormData();
    formData.append('user_query', query);
    formData.append('image', image);
    return API.post('/chat/image', formData); // No custom header needed
};

export const submitFeedback = (interactionId, isGood) => API.post(`/chat/feedback?interaction_id=${interactionId}&is_good=${isGood}`);

export const fetchChatHistory = () => API.get('/chat/history');