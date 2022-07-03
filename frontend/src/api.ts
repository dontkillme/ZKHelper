import axios from 'axios';
import { useBarAuthStore } from 'stores/BarAuth';

const axiosClient = axios.create({
	baseURL: process.env.API_URL,
	headers: {
		'Content-Type': 'application/json',
		'Cache-Control': 'no-cache',
		'Pragma': 'no-cache',
	},
});

// let requestCount = 0;

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
					throw {
						status: error.response.status,
						message: error.response.data.detail,
					};
				}
				throw {
					status: error.response.status,
					message: 'Api call failed without any details!',
				};
			} else if (error.request) {
				throw {
					status: null,
					message: `Api call failed on GET "${error.request.responseURL}" as no response received!`,
				};
			} else {
				throw {
					status: null,
					message: `Api call failed on request preparation failed! Error: ${error.message}`,
				};
			}
		}

		throw {
			status: null,
			message: `Unexpected Api error! Error: ${error}`,
		};
	}
);

// axiosClient.interceptors.request.use(
// 	(config) => {
// 		increaseRequestCounter();
// 		return config;
// 	},
// 	(error) => {
// 		decreaseRequestCounter(false);
// 		return Promise.reject(error);
// 	}
// );
//
// axiosClient.interceptors.response.use(
// 	(response) => {
// 		decreaseRequestCounter(true);
// 		return response;
// 	},
// 	(error) => {
// 		decreaseRequestCounter(false);
// 		return Promise.reject(error);
// 	}
// );
//
// function increaseRequestCounter() {
// 	requestCount += 1;
//
// 	if (requestCount === 1) {
// 		const loadingBar = useLoadingBar();
// 		loadingBar.start();
// 	}
// }
//
// function decreaseRequestCounter(success: bool) {
// 	requestCount -= 1;
//
// 	if (requestCount === 0) {
// 		const loadingBar = useLoadingBar();
//
// 		if (success) {
// 			loadingBar.finish();
// 		} else {
// 			loadingBar.error();
// 		}
// 	}
// }

export default axiosClient;
