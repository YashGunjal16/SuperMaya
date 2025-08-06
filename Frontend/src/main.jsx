import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx' // This will be our new router App
import './index.css'     // This will be our new global styles

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)