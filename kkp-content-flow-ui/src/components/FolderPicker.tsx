import React from 'react';

const FolderPicker: React.FC = ({ onPathChange }) => {
  const handleFolderSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = event.target.files;
    let file_path = "";
    if (files && files.length > 0) {
      file_path = files[0].webkitRelativePath || files[0].name;
      console.log('Selected file path:', file_path);
    }
    onPathChange("/Volumes/KKP.2024/Photos/Wedding/Blum.06.01/Finals/SEO.Web/" + file_path);
  };

  return (
    <div className="folder-picker-container">
        <label htmlFor="folderPicker">Choose an Alt Text SEO file:</label>
        <input
          type="file"
          accept=".csv"
          onChange={handleFolderSelect}
        />
    </div>
  );
};

export default FolderPicker;