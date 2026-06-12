import axios from 'axios';

const client = axios.create({
    baseURL: 'http://localhost:8000/api',
    headers: {
        'Content-Type': 'application/json',
    },
});

export const analyzeUrl = async (url) => {
    const response = await client.post('/analyze', { url });
    return response.data;
};

export const getHistory = async (page = 1, limit = 20, riskLevel = null) => {
    const params = { page, limit };
    if (riskLevel) params.risk_level = riskLevel;

    const response = await client.get('/history', { params });
    return response.data;
};

export const getStats = async () => {
    const response = await client.get('/stats');
    return response.data;
};

export default client;
