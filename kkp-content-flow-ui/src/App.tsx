
import React, { useState } from 'react';
import './App.css';
import FolderPicker from './components/FolderPicker.tsx';

function App() {
  const [output, setOutput] = useState('');

  const handleSubmit = () => {
    // For demonstration, we'll just set a static output
    setOutput('This is the output from the Submit button.');
  };

  return (
    <div className="App">
      <div className="content">
        <div className="left-column">
          <div className="user-input-container">
            <textarea placeholder="Enter your prompt here..."></textarea>
            <FolderPicker />
          </div>
          <div className="button-container">
            <button onClick={handleSubmit}>Submit</button>
          </div>
        </div>
        <div className="right-column">
          <div className="output-panel">
            {output}
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
