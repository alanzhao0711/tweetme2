import { backendlookup } from "../lookup/components"


export function apiTweetCreate(newTweet, callback){
    backendlookup("POST", "/tweets/create", callback, {content: newTweet})
}
export function apiTweetAction(tweetID, action, callback){
    const data = {id: tweetID, action: action}
    backendlookup("POST", "/tweets/action", callback, data)
}
export function apiTweetDetail(tweetID, callback) {
    backendlookup("GET", `/tweets/${tweetID}`, callback)

}
export function apiTweetList(username, callback) {
    let endpoint = "/tweets"
    if (username) {
        endpoint = `/tweets/?username=${username}`
    }
    backendlookup("GET", endpoint, callback)
}
    