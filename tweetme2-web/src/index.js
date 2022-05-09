import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import reportWebVitals from './reportWebVitals';
import { TweetDetailComponent, TweetsComponent, FeedComponent } from './tweets';
import { ProfileBadgeComponent } from './profiles';

const e = React.createElement
const tweetsEl = (document.getElementById('tweetme'));
const root = ReactDOM.createRoot(tweetsEl)
root.render(
  e(TweetsComponent, tweetsEl.dataset)
); 

const g = React.createElement
const tweetFeedElements = (document.getElementById("tweetme-2-feed"));
const feed = ReactDOM.createRoot(tweetFeedElements)
feed.render(
  g(FeedComponent, tweetFeedElements.dataset)
)

const tweetDetailElements = document.querySelectorAll(".tweetme-2-detail")
tweetDetailElements.forEach(container=> {
  const detail_render = ReactDOM.createRoot(container)
  detail_render.render(
    e(TweetDetailComponent, container.dataset)
  ); 
})

const t = React.createElement
const userProfileBadgeElements = document.querySelectorAll(".tweetme-2-profile-badge")
userProfileBadgeElements.forEach(container=> {
  const profile_render = ReactDOM.createRoot(container)
  profile_render.render(
    t(ProfileBadgeComponent, container.dataset)
  ); 
})
// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
