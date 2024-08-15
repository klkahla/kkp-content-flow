import React from 'react';

const FolderPicker: React.FC = () => {
  const handleFolderSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const folder = event.target.files;
    if (folder) {
      console.log('Selected folder:', folder);
    }
  };

  return (
    <div className="folder-picker-container">
        <label htmlFor="folderPicker">Choose an Alt Text SEO file:</label>
        <input
        type="file"
        webkitdirectory="true"
        directory="true"
        onChange={handleFolderSelect}
        />
    </div>
  );
};

export default FolderPicker;