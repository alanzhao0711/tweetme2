import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import reportWebVitals from './reportWebVitals';
import { TweetDetailComponent, TweetsComponent } from './tweets';

const e = React.createElement
const tweetsEl = (document.getElementById('tweetme'));
const root = ReactDOM.createRoot(tweetsEl)
root.render(
  e(TweetsComponent, tweetsEl.dataset)
); 

const tweetDetailElements = document.querySelectorAll(".tweetme-2-detail")

tweetDetailElements.forEach(container=> {
  const new_render = ReactDOM.createRoot(container)
  new_render.render(
    e(TweetDetailComponent, container.dataset)
  ); 
})
// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
