import React, { useState, useEffect } from 'react';

const initialChatMessages = [
  "Welcome to Intelligent Guard AI Surveillance System.",
  "This system provides advanced video processing capabilities.",
  "You can upload videos, paste video links, or use the webcam for processing.",
  "Processed videos can be downloaded for further analysis.",
  "If you have any questions, feel free to ask!",
  "this system has the ability to detect object through video or camera",
  "if you facing any issues contact SUPPORT",
  "Contact us thinkbig8759@gmail.com",
  "keep your environment safe & Secured"
];

const ChatBox = () => {
  const [chatMessages, setChatMessages] = useState(initialChatMessages);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [speaking, setSpeaking] = useState(false);

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentIndex(prevIndex => (prevIndex + 1) % initialChatMessages.length);
    }, 5000); // Change message every 5 seconds
    return () => clearInterval(interval);
  }, []);

  const handleReadMessage = () => {
    setSpeaking(true);
    const synth = window.speechSynthesis;
    const utterance = new SpeechSynthesisUtterance(initialChatMessages[currentIndex]);
    utterance.onend = () => {
      setSpeaking(false);
    };
    synth.speak(utterance);
  };

  return (
    <div style={{ position: 'absolute', bottom: '20px', right: '20px' }}>
      <div className="chat-box">
        <p>{chatMessages[currentIndex]}</p>
        <button onClick={handleReadMessage} disabled={speaking}>Read Message</button>
      </div>
    </div>
  );
};

export default ChatBox;
