import React from 'react';
import { Link } from 'react-router-dom';
import './homepage.css';

function HomePage() {
    return (
        <div className="container">
            <header>
                <h1>Welcome to Heart Health Checker</h1>
            </header>
            <main>
                <section>
                    <h2>Your Partner in Monitoring Heart Health</h2>
                    <p>At Heart Health Checker, we are dedicated to helping you understand and manage your heart health. Our advanced risk assessment tool uses state-of-the-art machine learning algorithms to evaluate your risk of heart disease based on key health indicators.</p>
                </section>
                <section>
                    <h2>Start Your Heart Health Journey Today</h2>
                    <p>Take the first step towards a healthier heart. Use our Heart Health Checker tool to understand your risk and make informed decisions about your health.</p>
                </section>
                <section>
                    <h2>Prevention and Management</h2>
                    <p>Maintaining a healthy lifestyle, including a balanced diet, regular exercise, and avoiding smoking, can help reduce your risk of heart disease.</p>
                    <Link to="/input" className="cta-button">Get Started Now</Link>
                </section>
            </main>
            <footer>
                <p>&copy; 2024 Heart Disease Awareness</p>
            </footer>
        </div>
    );
}

export default HomePage;
