import React, { useState, useEffect, useRef } from 'react';
import ChatMessage from '../components/ChatMessage.jsx';
import { postTextQuery, postImageQuery, fetchChatHistory } from '../api/index.js';

export default function ChatPage({ onLogout }) {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const [imageFile, setImageFile] = useState(null);
    const [isThinking, setIsThinking] = useState(false);
    const messagesEndRef = useRef(null);
    const fileInputRef = useRef(null);

    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [messages]);

    const handleSend = async (queryOverride) => {
        const currentQuery = queryOverride || input;
        if (!currentQuery.trim() && !imageFile) return;

        const userMessage = { sender: 'user', text: currentQuery };
        setMessages(prev => [...prev, userMessage]);
        
        setInput('');
        setImageFile(null);
        setIsThinking(true);

        try {
            let response;
            if (imageFile) {
                response = await postImageQuery(currentQuery, imageFile);
            } else {
                response = await postTextQuery(currentQuery);
            }
            const aiMessage = { sender: 'ai', text: response.data.ai_response, interactionId: response.data.id };
            setMessages(prev => [...prev, aiMessage]);
        } catch (error) {
            console.error("Error in handleSend:", error);
            const errorMessage = { sender: 'ai', text: 'An error occurred. Please check the console and backend logs.' };
            setMessages(prev => [...prev, errorMessage]);
        } finally {
            setIsThinking(false);
        }
    };

    const handleTagClick = (tag) => {
        handleSend(`Tell me more about ${tag}`);
    };

    return (
        <div className="chat-container">
            <header className="chat-header">
                <h1>SuperMaya Workspace</h1>
                <button className="logout-btn" onClick={onLogout}>Logout</button>
            </header>
            <div className="message-list">
                {messages.map((msg, index) => (<ChatMessage key={index} message={msg} onTagClick={handleTagClick} />))}
                {isThinking && <div className="message ai thinking"><span>.</span><span>.</span><span>.</span></div>}
                <div ref={messagesEndRef} />
            </div>
            <div className="input-area">
                <button className="attach-btn" title="Attach Image" onClick={() => fileInputRef.current.click()}>📎</button>
                <input type="file" ref={fileInputRef} onChange={e => setImageFile(e.target.files[0])} style={{ display: 'none' }} accept="image/*" />
                <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && !isThinking ? handleSend() : null}
                    placeholder={imageFile ? `Ask about ${imageFile.name}...` : "Ask anything or attach an image..."}
                    disabled={isThinking}
                />
                <button className="send-btn" title="Send" onClick={() => handleSend()} disabled={isThinking}>➤</button>
            </div>
        </div>
    );
}