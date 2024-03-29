import {
	CATEGORIES_LIST_REQUEST,
	CATEGORIES_LIST_SUCCESS,
	CATEGORIES_LIST_FAIL,
	CATEGORIES_DELETE_FAIL,
	CATEGORIES_DELETE_REQUEST,
	CATEGORIES_DELETE_SUCCESS,
	CATEGORIES_ADD_FAIL,
	CATEGORIES_ADD_REQUEST,
	CATEGORIES_ADD_SUCCESS,
	CATEGORIES_EDIT_FAIL,
	CATEGORIES_EDIT_REQUEST,
	CATEGORIES_EDIT_SUCCESS,
} from "../constants/catagoriesConstants";
import axios from "axios";
import { url } from "../constants/host";

export const categoriesList = () => async (dispatch) => {
	try {
		dispatch({
			type: CATEGORIES_LIST_REQUEST,
		});

		const config = {
			headers: {
				"Content-type": "application/json",
			},
		};

		const { data } = await axios.post(
			`${url}/graphql`,
			{
				query: `
                query{
                    categories{
                        edges{
                            node{
                                id
                                name
                                postsCount
                            }
                        }
                    }
                }
            `,
			},
			config
		);

		dispatch({
			type: CATEGORIES_LIST_SUCCESS,
			payload: data.data.categories.edges,
		});
	} catch (error) {
		dispatch({
			type: CATEGORIES_LIST_FAIL,
			payload:
				error.respone && error.response.data.detail
					? error.response.data.detail
					: error.message,
		});
	}
};

export const deleteCategories = (id) => async (dispatch, getState) => {
	try {
		dispatch({
			type: CATEGORIES_DELETE_REQUEST,
		});

		const config = {
			headers: {
				"Content-type": "application/json",
				"Sec-Fetch-Dest": "empty",
				"Sec-Fetch-Mode": "cors",
				"Sec-Fetch-Site": "same-origin",
			},
		};

		const { data } = await axios.post(
			`${url}/graphql`,
			{
				query: `
                mutation{
                    deleteCategory(categoryId: "${id}"){
                        success
                        errors
                    }
                }
            `,
			},
			config,
			{
				withCredentials: true,
			}
		);

		dispatch({
			type: CATEGORIES_DELETE_SUCCESS,
		});
	} catch (error) {
		dispatch({
			type: CATEGORIES_DELETE_FAIL,
			payload:
				error.response && error.response.data.detail
					? error.response.data.detail
					: error.message,
		});
	}
};

export const createCategory = (name) => async (dispatch, getState) => {
	try {
		dispatch({
			type: CATEGORIES_ADD_REQUEST,
		});

		const config = {
			headers: {
				"Content-type": "application/json",
				"Sec-Fetch-Dest": "empty",
				"Sec-Fetch-Mode": "cors",
				"Sec-Fetch-Site": "same-origin",
			},
		};
		const { data } = await axios.post(
			`${url}/graphql`,
			{
				query: `
                mutation{
                    createCategory(name: "${name}"){
                        category{
                            id
                            name
                        }
                    }
                }
            `,
			},
			config,
			{
				withCredentials: true,
			}
		);

		console.log(data);

		dispatch({
			type: CATEGORIES_ADD_SUCCESS,
			payload: data,
		});
	} catch (error) {
		dispatch({
			type: CATEGORIES_ADD_FAIL,
			payload:
				error.response && error.response.data.detail
					? error.response.data.detail
					: error.message,
		});
	}
};

export const editCategory = (category) => async (dispatch, getState) => {
	try {
		dispatch({
			type: CATEGORIES_EDIT_REQUEST,
		});

		const {
			userLogin: { userInfo },
		} = getState();

		const config = {
			headers: {
				"Content-type": "application/json",
			},
		};
		const { data } = await axios.post(
			`${url}/graphql`,
			{
				query: `
                mutation{
                    updateCategory(categoryId: "${category.id}", name: "${category.name}"){
                        category{
                            id
                            name
                        }
                    }
                }
            `,
			},
			config
		);

		dispatch({
			type: CATEGORIES_EDIT_SUCCESS,
			payload: data,
		});
	} catch (error) {
		dispatch({
			type: CATEGORIES_EDIT_FAIL,
			payload:
				error.response && error.response.data.detail
					? error.response.data.detail
					: error.message,
		});
	}
};
