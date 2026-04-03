import axios from 'axios';

const API = axios.create({
  baseURL: 'https://your-backend-url.com', // TODO: Replace with real backend
});

// Example API calls

export const sendOtp = (phone: string) => {
  // TODO: CONNECT BACKEND
  return API.post('/send-otp', { phone });
};

export const verifyOtp = (phone: string, otp: string) => {
  // TODO: CONNECT BACKEND
  return API.post('/verify-otp', { phone, otp });
};

export const getDashboard = () => {
  // TODO: CONNECT BACKEND
  return API.get('/dashboard');
};

export default API;