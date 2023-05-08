import React, { useEffect, useState } from "react";
import axios from "axios";
import PostList from "../components/PostList";
import Loader from "../components/Loader";
import { categoriesList } from "../actions/categoriesActions";
import CategoryItem from "../components/CategoryItem";
import { useDispatch, useSelector } from "react-redux";

import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
import "firebase/auth";
import firebaseConfig from "../firebaseConfig.json";
import "firebase/firestore";
import "firebase/storage";
import Dropdown from 'react-bootstrap/Dropdown';
import DropdownButton from 'react-bootstrap/DropdownButton';
import {url} from '../constants/host'
const PAGE_NUMBER = 0;

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);

const HomeScreen = () => {
  const dispatch = useDispatch();

    const [postData, setPostData] = useState([]);
    const [page, setPage] = useState(PAGE_NUMBER);
    const [loading, setLoading] = useState(true);

  const [hasNextPage, setHasNextPage] = useState(true);

  const CategoriesList = useSelector((state) => state.categoriesList);
  const { error, categories } = CategoriesList;

  useEffect(() => {
    dispatch(categoriesList());
  }, [dispatch]);

  useEffect(() => {
    setTimeout(async () => {
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
              posts(first: 12, offset: ${page}){
                  edges{
                    node{
                      id
                      title
                      description
                      likes
                      dislikes
                      createTime
                      isLiked
                      isDisliked
                      commentsCount
                      image{
                        url
                      }
                      user{
                          username
                      }
                    }
                  }
                    pageInfo{
                    hasNextPage
                    }
                }
                }
                `
        }, config);

        if (!data.data.posts.pageInfo.hasNextPage) {
            setHasNextPage(false);
        }
        if (data.data.posts.edges.length > 0) {
            setPostData((prev) => [...prev, ...data.data.posts.edges]);
        }
        setLoading(false);
    }, 1000);
    }, [page]);

  useEffect(() => {
    if (hasNextPage) {
      window.addEventListener("scroll", handleScroll);
    } else {
      window.removeEventListener("scroll", handleScroll);
    }
    return () => window.removeEventListener("scroll", handleScroll);
  }, [hasNextPage]);

  const handleScroll = async () => {
    if (
      window.innerHeight + document.documentElement.scrollTop + 1 >=
      document.documentElement.scrollHeight
    ) {
      setLoading(true);
      setPage((prev) => prev + 12);
    }
  };

  return (
    <div className="app">
      EXPLORE TAGS <br></br>
      <div className="categories">
        {categories.map((category) => (
          <CategoryItem name={category.node.name} postsCount={category.node.postsCount} id={category.node.id}/>
        ))}
      </div>
        <br></br>
      <Dropdown className="sort">
        <Dropdown.Toggle id="dropdown-button-dark-example1" variant="success" className="sort-btn">
          Sort by
        </Dropdown.Toggle>

        <Dropdown.Menu variant="dark">
          <Dropdown.Item href="/" active> Newest </Dropdown.Item>
          <button onClick={() => console.log("ELOELO")}><Dropdown.Item active> Best rating </Dropdown.Item></button>
          <Dropdown.Item href="#/action-1" active> Popularity </Dropdown.Item>
        </Dropdown.Menu>
      </Dropdown>
      <PostList posts={postData} />
      {loading && <Loader />}
    </div>
  );
};

export default HomeScreen;