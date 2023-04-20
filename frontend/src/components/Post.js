import React, { useState, useEffect } from "react";
import { Card } from 'react-bootstrap';
import { Link } from 'react-router-dom'
import {Button} from 'react-bootstrap'

function Post({post, my}) {

  const [hoveredItemId, setHoveredItemId] = useState(null);
  

  const handleItemMouseEnter = (itemId) => {
    setHoveredItemId(itemId);
  };

  const handleItemMouseLeave = () => {
    setHoveredItemId(null);
  };

  return (
    <div>
    {my ? 
      <Card className="my-3 rounded card-m" onMouseEnter={() => handleItemMouseEnter(post?.node?.id)} onMouseLeave={handleItemMouseLeave}>
        {post.node.id == hoveredItemId ? 
        (
        <div className='centering '>
          <Button variant='light' className="edit-btn mb-2"><i class="fa-solid fa-pen-to-square"></i> Edit</Button>
          <Button variant='primary' className="delete-btn"><i class="fa-regular fa-trash-can"></i> Delete</Button>
        </div>
        ) : null}
        <Link to={`/post/${post.node.id}`}>
          <Card.Img
            className={`scale-90	 max-h-72 ${post.node.id == hoveredItemId ? 'opacity-30' : null}`}
            src={`${post?.node.image?.url}`}
          />
        </Link>

        <Card.Body>
          <Card.Title className="text-center">
            <strong>{post.node.title}</strong>
          </Card.Title>

          <Card.Text as="div">
            <div className="my-3 text-xl flex justify-between px-4">
              <p className=""><i class="fa-regular fa-thumbs-up"></i> {post.node.likes}</p> 
              <p> <i class="fa-regular fa-thumbs-down"></i> {post.node.dislikes}</p>
              <p><i class="fa-regular fa-comment-dots"></i> {post.node.commentsCount}</p>
            </div>
          </Card.Text>
        </Card.Body>
      </Card>
    :
    <Card className="my-3 rounded hover:opacity-80">
      <Link to={`/post/${post.node.id}`}>
        <Card.Img
          className="scale-90	 max-h-72"
          src={`${post?.node.image?.url}`}
        />
      </Link>

      <Card.Body>
        <Card.Title className="text-center">
          <strong>{post.node.title}</strong>
        </Card.Title>

        <Card.Text as="div">
          <div className="my-3 text-xl flex justify-between px-4">
            <p className=""><i class="fa-regular fa-thumbs-up"></i> {post.node.likes}</p> 
            <p> <i class="fa-regular fa-thumbs-down"></i> {post.node.dislikes}</p>
            <p><i class="fa-regular fa-comment-dots"></i> {post.node.commentsCount}</p>
          </div>
        </Card.Text>
      </Card.Body>
    </Card>
    }
  </div>
  );
}

export default Post
