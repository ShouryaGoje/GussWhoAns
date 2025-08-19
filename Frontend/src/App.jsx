import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <h1> Guess Who Answered</h1>
      <form className='username-form'>
        <div className='form-row'>
          <label>Enter Username</label>
          <input type='text' id='username'>
          </input>
        </div>
        <button className='btn'>Ready!</button>

      </form>
      <button className='help-btn'>?</button>
    </>
  )
}

export default App
