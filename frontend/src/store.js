import { createStore, combineReducers, applyMiddleware } from 'redux'
import thunk from 'redux-thunk'
import { composeWithDevTools } from 'redux-devtools-extension'
import { userLoginReducer, userRegisterReducer, userUpdateProfileRecuder, userListReducer, userDeleteReducer, userDetailsReducer} from './reducers/userReducers'
import { categoriesListReducers, categoryDeleteReducer, categoriesCreateReducers, categoriesEditeReducers } from './reducers/categoriesReducers'
import { postListReducers, potsDetailsReducers, postCreateReducers, postCommentsReducers, addCommentReducers, commentDeleteReducer, commentEditeReducers } from './reducers/postReducers'



const reducer = combineReducers({
    userLogin: userLoginReducer,
    userRegister: userRegisterReducer,
    userUpdateProfile: userUpdateProfileRecuder,
    userList: userListReducer,
    userDelete: userDeleteReducer,
    userDetails: userDetailsReducer,
    categoriesList: categoriesListReducers,
    categoriesDelete: categoryDeleteReducer,
    categoriesCreate: categoriesCreateReducers,
    categoriesEdit: categoriesEditeReducers,
    postList: postListReducers,
    postDetails: potsDetailsReducers,
    postComments: postCommentsReducers,
    addComment: addCommentReducers,
    deleteComment: commentDeleteReducer,
    editComment: commentEditeReducers,
    postCreate: postCreateReducers,

})



const userInfoFromStorage = localStorage.getItem('userInfo') ?
    JSON.parse(localStorage.getItem('userInfo')) : null


const initialState = {
    userLogin: {userInfo: userInfoFromStorage},
}

const middleware = [thunk]

const store = createStore(reducer, initialState, composeWithDevTools(applyMiddleware(...middleware)))

export default store
