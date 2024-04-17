import { ChangeEvent, useState } from 'react'
import './App.css'
import axios from 'axios';

function App() {
  const [response, setResponse] = useState('');
  const [inputValue, setInputValue] = useState('');

  function handle_click(){
    const request = {'query': inputValue}
    axios.get('http://localhost:8000/api/test-query/', {
      params: request
    })
    .then(response => {
      setResponse(response.data.response);
      console.log(`Received: ${response.data.response}`)
    })
    .catch(error => {
      console.log(error);
    });
  }
  
  const handleInputChange = (event: ChangeEvent<HTMLInputElement>) => {
    setInputValue(event.target.value);
  };

  return (
    <>
      <div>
        <input 
        type="text"
        value={inputValue}
        onChange={handleInputChange}
        />
        <button onClick={handle_click}>Send</button>
      </div>
      <p>{response}</p>
    </>
  )
}

export default App
