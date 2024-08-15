
import React from 'react';
import './App.css';
import FolderPicker from './components/FolderPicker.tsx';

function App() {
  return (
    <div className="App">
      <div className="content">
        <div className="left-column">
          <div className="user-input-container">
            <textarea placeholder="Enter your prompt here..."></textarea>
            <FolderPicker />
          </div>
          <div className="button-container">
            <button>Submit</button>
          </div>
        </div>
        <div className="right-column">
          
        </div>
      </div>
    </div>
  );
}

export default App;
