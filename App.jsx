import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { Cloudinary } from '@cloudinary/url-gen';
import { AdvancedVideo } from '@cloudinary/react';
import './App.css';
import './button.css';
import './container.css';
import auth from './firebase/firebase';
import ChatBox from './ChatBox';
import FrameViewer from './FrameViewer';

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
      // Set the processed video public ID received from the backend response
      setProcessedVideoPublicId(response.data.processed_public_id);
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
  
  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleDownloadVideo = async () => {
    try {
      const response = await axios.get('http://localhost:5000/video', {
        responseType: 'blob',
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
      <div className="vertical-container">
        <h1 className="title white-colour">INTELLIGENT GUARD AI SURVEILLANCE SYSTEM</h1>
        <div className="form-container">
          <div className="button-container">
            <label htmlFor="video-file" style={{ color: 'white' }}>Choose a video file</label>
            <input type="file" accept="video/mp4" id="video-file" onChange={handleFileChange} />
            <button onClick={handleUpload} disabled={!file || processing} className="upload-button" style={{ width: '150px', height: '40px', fontSize: '15px' }}>
              {processing ? 'Processing...' : 'Upload Video'}
            </button>
          </div>
          <div className="button-container">
            <label htmlFor="video-link" style={{ color: 'white', fontSize: '15px' }}>Paste a video link:</label>
            <input type="text" id="video-link" value={videoLink} onChange={handleChange} placeholder="Paste Video Link" style={{ marginRight: '1rem', width: '150px', height: '15px', fontSize: '8px' }} />
            <button onClick={handlePasteLink} className="play-button" style={{ width: '150px', height: '40px', fontSize: '15px' }}>Play Video</button>
          </div>
          {processedVideoPublicId && (
            <div className="button-container">
              <button onClick={handleDownloadVideo} className="download-button" style={{ width: '230px', height: '40px', fontSize: '15px' }}>Download Processed Video</button>
            </div>
          )}
          <div className="button-container">
            <button onClick={handleCameraDetection} className="camera-detection-button" style={{ width: '150px', height: '40px', fontSize: '15px' }}>Turn On Camera</button>
          </div>
          <div style={{ position: 'absolute', top: 15, right: 10, marginTop: '15px', marginRight: '15px' }}>
            <button onClick={handleLogout} className="logout-button" style={{ backgroundColor: 'red', width: '100px', height: '40px', fontSize: '14px' }}>Logout</button>
          </div>
        </div>
        <FrameViewer />
        {processedVideoPublicId && (
          <div className="video-container">
            <AdvancedVideo
              cldVid={cloudinary.video(processedVideoPublicId)}
              width='57%'
              height='60%'
              controls
              key={processedVideoPublicId}
            />
          </div>
        )}
      </div>
      <ChatBox />
    </main>
  );
}

export default App;
