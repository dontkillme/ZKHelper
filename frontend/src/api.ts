import axios from 'axios';
import { useBarAuthStore } from '@/stores/BarAuth';

const axiosClient = axios.create({
	baseURL: import.meta.env.VITE_API_URL,
	headers: {
		'Content-Type': 'application/json',
	},
});

axiosClient.interceptors.request.use((config) => {
	const { token } = useBarAuthStore();

	if (!config.headers) {
		config.headers = {};
	}

	config.headers.Authorization = token ? `token ${token}` : '';

	return config;
});

axiosClient.interceptors.response.use(
	(response) => response,
	(error) => {
		if (axios.isAxiosError(error)) {
			if (error.response) {
				if (error.response.data?.detail) {
					throw new Error(error.response.data.detail);
				}
				throw new Error(
					`Api call failed on GET "${error.request.responseURL}" with status code "${error.response.status}"!`
				);
			} else if (error.request) {
				throw new Error(`Api call failed on GET "${error.request.responseURL}" as no response received!`);
			} else {
				throw new Error(`Api call failed on request preparation failed! Error: ${error.message}`);
			}
		}

		throw new Error(`Unexpected Api error! Error: ${error}`);
	}
);

export default axiosClient;
