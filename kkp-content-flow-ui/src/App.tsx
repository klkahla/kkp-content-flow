
import React, { useState } from 'react';
import './App.css';
import FolderPicker from './components/FolderPicker.tsx';
import { createContentWorkflow } from './api/api.tsx';

function App() {
  const [prompt, setPrompt] = useState('');
  const [csvFilePath, setCsvFilePath] = useState('');
  const [output, setOutput] = useState('');
  const [loading, setLoading] = useState(false);

  const handlePromptChange = (event: React.ChangeEvent<HTMLTextAreaElement>) => {
    setPrompt(event.target.value);
  };

  const handleCsvFilePathChange = (path: string) => {
    console.log('Path changed: ' + path);
    setCsvFilePath(path);
  };
  
  const handleSubmit = async () => {
    setLoading(true);
    try {
      const response = await createContentWorkflow(prompt, csvFilePath);
      setOutput(response.content);
    } catch (error) {
      setOutput('An error occurred while processing your request.');
    } finally {
      setLoading(false);
    }
  };


  return (
    <div className="App">
      <div className="content">
        <div className="left-column">
          <div className="user-input-container">
          <textarea 
              placeholder="Enter your prompt here..." 
              value={prompt} 
              onChange={handlePromptChange}
            />
            <FolderPicker onPathChange={handleCsvFilePathChange} />
          </div>
          <div className="button-container">
            <button onClick={handleSubmit} disabled={loading}>
              {loading ? 'Processing...' : 'Submit'}
            </button>
          </div>
        </div>
        <div className="right-column">
          <div className="output-panel">
            {loading ? 'Loading...' : output}
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
