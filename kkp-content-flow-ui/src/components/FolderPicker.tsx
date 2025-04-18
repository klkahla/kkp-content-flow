import React from 'react';

const FolderPicker: React.FC = ({ onPathChange }) => {
  const handleFolderSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    onPathChange(event.target.value);
  };

  return (
    <div className="folder-picker-container">
      <label htmlFor="folderPicker">Choose an Alt Text SEO file:</label>
      <input
        type="text"
        placeholder='Enter file path'
        onChange={handleFolderSelect}
        style={{ width: '100%' }}
      />
    </div>
  );
};

export default FolderPicker;