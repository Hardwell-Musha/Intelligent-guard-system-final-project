const express = require('express');
const path = require('path');

const app = express();

// Serve static files from the processed_video directory
app.use('/processed_video', express.static(path.join(__dirname, 'client', 'processedvideo')));

// Handle POST request to process video
app.post('/process-video', async (req, res) => {
    // Implement video processing logic here
    // This route is responsible for processing the uploaded video and saving it to the processed_video directory
    // Once processing is complete, respond with the URL to the processed video
    const processedVideoUrl = 'http://localhost:5000/processedvideo.mp4';
    res.json({ videoUrl: processedVideoUrl });
});

// Start the server
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
