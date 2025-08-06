import React from 'react';
import { submitFeedback } from '../api/index.js';
import VegaChart from './VegaChart.jsx'; // <-- IMPORT THE NEW UNIVERSAL COMPONENT

export default function ChatMessage({ message, onTagClick }) {
    const { sender, text, interactionId } = message;

    const handleFeedback = async (isGood) => {
        if (!interactionId) return;
        try {
            await submitFeedback(interactionId, isGood);
            alert('Feedback submitted!');
        } catch (error) {
            console.error('Failed to submit feedback', error);
        }
    };

    // --- Main Renderer ---

    // This block handles all messages from the AI
    if (sender === 'ai') {
        // First, check if the 'text' is a valid, non-empty string that looks like JSON.
        // This is the core of the bug fix. It prevents crashes from null, undefined, or simple string responses.
        if (typeof text === 'string' && text.trim().startsWith('{')) {
            try {
                const data = JSON.parse(text);

                // Case 1: FinancialResponse (has chart_data)
                if (data.visualization_spec) {
                return (
                    <div className="message ai">
                        <p>{data.primary_response}</p>
                        <VegaChart spec={data.visualization_spec} />
                        <div className="feedback-buttons">{/* ... */}</div>
                    </div>
                );
            }
            
                // Case 2: VisionResponse (has image_description)
                if (data.image_description) {
                    return (
                        <div className="message ai vision-response">
                            <p><strong>Image Analysis:</strong> {data.image_description}</p>
                            <p><strong>Answer:</strong> {data.user_query_answer}</p>
                            <div className="object-tags">
                                {data.identified_objects.map((obj, i) => (
                                    <button key={i} className="tag-button" onClick={() => onTagClick(obj)}>
                                        {obj}
                                    </button>
                                ))}
                            </div>
                            <div className="feedback-buttons">
                                <button onClick={() => handleFeedback(true)}>👍</button>
                                <button onClick={() => handleFeedback(false)}>👎</button>
                            </div>
                        </div>
                    );
                }

                // Case 3: Rich TextResponse (has primary_response)
                if (data.primary_response) {
                    return (
                        <div className="message ai">
                            {data.primary_response}
                            {data.image_url && <img src={data.image_url} alt="AI generated visual" className="ai-image"/>}
                            {data.reference_links && (
                                <div className="reference-links">
                                    <strong>Learn More:</strong>
                                    <ul>{data.reference_links.map((link, i) => <li key={i}><a href={link} target="_blank" rel="noopener noreferrer">{link}</a></li>)}</ul>
                                </div>
                            )}
                            <div className="feedback-buttons">
                                <button onClick={() => handleFeedback(true)}>👍</button>
                                <button onClick={() => handleFeedback(false)}>👎</button>
                            </div>
                        </div>
                    );
                }
            } catch (e) {
                // If parsing fails, it will fall through and render the raw text below.
                console.error("JSON parsing failed, rendering raw text:", text);
            }
        }
        
        // This is the fallback renderer. It will display:
        // 1. Any AI message that was not valid JSON (like a simple error string).
        // 2. Any AI message that was valid JSON but didn't match our known structures.
        return (
            <div className="message ai">
                {text || "Received an empty response."} 
            </div>
        );
    }

    // This renders all user messages
    return (
        <div className={`message ${sender}`}>
            {text}
        </div>
    );
}