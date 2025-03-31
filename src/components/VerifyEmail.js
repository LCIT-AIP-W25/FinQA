import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import axios from "axios";

function VerifyEmail() {
    const { token } = useParams();
    const navigate = useNavigate();
    const [message, setMessage] = useState("");

    useEffect(() => {
        const verify = async () => {
            try {
                const response = await axios.get(`http://127.0.0.1:5001/verify_email/${token}`);
                
                if (response.status === 200) {
                    setMessage("✅ Email verified! Redirecting to login...");
                    setTimeout(() => navigate("/login"), 3000);
                } else {
                    setMessage("❌ " + response.data.message);
                }
            } catch (error) {
                setMessage("❌ Verification failed. Invalid or expired link.");
            }
        };
    
        verify();
    }, [token, navigate]);
     

    return (
        <div className="verify-container">
            <h2>Email Verification</h2>
            <p>{message}</p>
        </div>
    );
}

export default VerifyEmail;
