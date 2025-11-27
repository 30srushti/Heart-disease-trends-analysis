import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom'; // Import useNavigate
import './resultpage.css'; // Import the CSS file for styling

function ResultPage() {
    const location = useLocation();
    const navigate = useNavigate(); // Use useNavigate
    
    // Extract result from state passed through navigate
    const { result } = location.state || {}; // Provide a default empty object if result is not available

    const handleReturnHome = () => {
        navigate('/'); // Use navigate instead of history.push
    };

    const handleNewAssessment = () => {
        navigate('/input'); 
    };

    return (
        <div className="container">
            <h1>Heart Disease Risk Assessment Result</h1>
            <div className="result">
                {result ? (
                    <div>
                        <h2>Your Risk Prediction</h2>
                        <p><strong>Risk Level:</strong> {result.predicted_heart_disease ? "High" : "Low"}</p>
                        <p><strong>Details:</strong> {result.details || "No additional details available."}</p>
                    </div>
                ) : (
                    <p>No result available. Please try again.</p>
                )}
            </div>
            <div className="actions">
                <button onClick={handleReturnHome}>Return to Home</button>
                <button onClick={handleNewAssessment}>Start New Assessment</button>
            </div>
        </div>
    );
}

export default ResultPage;
