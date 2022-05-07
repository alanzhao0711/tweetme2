import React from 'react'
import { apiTweetCreate } from './lookup'


export function TweetCreate(props) { 
  const textareaRef = React.createRef()
  const {didTweet} = props
  const handleBackendUpdate = (response, status) => {
    if (status === 201) {
      didTweet(response)
    } else {
      console.log(response)
      alert("An error occured please try again")
    }
  }
  const handleSubmit = (event) => {
    event.preventDefault()
    const newVal = textareaRef.current.value
    // backend api request
    apiTweetCreate(newVal, handleBackendUpdate)
    textareaRef.current.value = ''
  }
  return <div className={props.className}>
    <form onSubmit={handleSubmit}> 
      <textarea ref={textareaRef} required={true} className='form-control' name='tweet'>

      </textarea>
      <button type='submit' className='btn btn-primary my-3'>Tweet</button>
    </form>
    </div>
}