import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { Cloudinary } from '@cloudinary/url-gen';
import { AdvancedVideo } from '@cloudinary/react';
import './App.css';
import './button.css';
import './container.css';
import auth from './firebase/firebase';
import ChatBox from './ChatBox'; // Import the ChatBox component

const cloudinary = new Cloudinary({
  cloud: {
    cloudName: 'diykglllj' 
  }
});

function App() {
  const navigate = useNavigate();
  const [file, setFile] = useState(null);
  const [processing, setProcessing] = useState(false);
  const [processedVideoPublicId, setProcessedVideoPublicId] = useState('');
  const [videoLink, setVideoLink] = useState('');

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleChange = (e) => {
    setVideoLink(e.target.value);
  };

  const handleUpload = async () => {
    setProcessing(true);
    const formData = new FormData();
    formData.append('file', file);
    try {
      const response = await axios.post('http://localhost:5000/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      setProcessedVideoPublicId(response.data.processed_video_url);
    } catch (error) {
      console.error('Error uploading file:', error);
    } finally {
      setProcessing(false);
    }
  };

  const handlePasteLink = () => {
    setProcessedVideoPublicId(videoLink);
  };

  const handleCameraDetection = async () => {
    try {
      const response = await axios.post('http://localhost:5000/webcam');
      setProcessedVideoPublicId(response.data.processed_video_url);
    } catch (error) {
      console.error('Error processing webcam:', error);
    }
  };

  const handleDownloadVideo = async () => {
    try {
      const response = await axios.get('http://localhost:5000/video', {
        responseType: 'blob', // Important: responseType as 'blob' for binary data
      });
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'processed_video.mp4');
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error('Error downloading video:', error);
    }
  };

  const handleLogout = () => {
    auth.signOut();
    navigate('/login');
  };

  return (
    <main className="main">
      <div className="container">
        <h1 className="title blue-color">Intelligent Guard AI Surveillance System</h1>
        <div className="form-container">
          <div className="file-input-container">
            <div className="file-button-container">
              <label htmlFor="video-file" style={{ color: 'white' }}>Choose a video file</label>
              <input type="file" accept="video/mp4" id="video-file" onChange={handleFileChange} />
              <button onClick={handleUpload} disabled={!file || processing} className="upload-button">
                {processing ? 'Processing...' : 'Upload Video'}
              </button>
            </div>
            <div className="link-container">
              <label htmlFor="video-link" style={{ color: 'white' }}>paste a video link:</label>
              <input type="text" id="video-link" value={videoLink} onChange={handleChange} placeholder="Paste Video Link" style={{ marginRight: '1rem' }} />
              <button onClick={handlePasteLink} className="play-button">Play Video</button>
            </div>
          </div>
          {processedVideoPublicId && (
            <>
              <button onClick={handleDownloadVideo} className="download-button" style={{ marginBottom: '1rem' }}>Download Processed Video</button>
            </>
          )}
          <button onClick={handleCameraDetection} className="camera-detection-button">Turn On Camera</button>
          <div style={{ marginTop: '10px', textAlign: 'right' }}>
            <button onClick={handleLogout} className="logout-button" style={{ backgroundColor: 'red' }}>Logout</button>
          </div>
        </div>
      </div>
      <ChatBox /> {/* Add the ChatBox component here */}
      {processedVideoPublicId && (
        <div className="video-container" style={{ marginTop: '20px', display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
          <AdvancedVideo
            cldVid={cloudinary.video(processedVideoPublicId)}
            width='50%'
            height='50%'
            controls
            key={processedVideoPublicId} // Add key to force re-render when video changes
          />
        </div>
      )}
    </main>
  );
}

export default App;
