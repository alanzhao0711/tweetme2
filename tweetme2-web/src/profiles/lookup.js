import { backendlookup } from "../lookup/components"


export function apiProfileDetail(username, callback) {
    backendlookup("GET", `/profiles/${username}`, callback)

}

export function apiProfileFollowToggle(username, action, callback) {
    const data = {action: `${action && action}`.toLowerCase()}
    backendlookup("POST", `/profiles/${username}/follow`, callback, data)

}