import { useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import axios from "axios";
import { useLoader } from "./LoaderContext";
import 'bootstrap/dist/css/bootstrap.min.css';

function ResetPassword() {
    const { token } = useParams(); // ✅ Get token from URL
    const navigate = useNavigate();
    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    const [message, setMessage] = useState("");
    const { setLoading } = useLoader();

    const handleReset = async (e) => {
        e.preventDefault();
        setMessage(""); // Clear old messages

        if (!password || password.length < 6) {
            setMessage("❌ Password must be at least 6 characters.");
            return;
        }

        if (password !== confirmPassword) {
            setMessage("❌ Passwords do not match.");
            return;
        }

        try {
            setLoading(true);
            const response = await axios.post("http://127.0.0.1:5001/reset_password", {
                token,
                password
            });

            if (response.data.status === "success") {
                setMessage("✅ Password reset successful! Redirecting to login...");
                setTimeout(() => navigate("/login"), 3000);
            } else {
                setMessage("❌ " + response.data.message);
            }
        } catch (err) {
            setMessage("❌ Failed to reset password. Try again.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <section className='sec-reset'>
            <div className='container-fluid'>
                <div className='row height-row'>
                    <div className='col-6 col-top'>
                        <div className='d-flex justify-content-center'>
                            <div className='box-size'>
                                <div className='d-flex align-items-center box-pad'>
                                    <img className='inline-block' src='/images/we.png' alt="Logo" />
                                </div>
                                <p className='wel-txt'>Reset Your Password</p>
                                <p className='det-txt'>Enter a new password to secure your account.</p>

                                {message && <p className="message">{message}</p>}

                                <form className='form-space' onSubmit={handleReset}>
                                    <label className='txt-lab'>New Password</label>
                                    <input
                                        type="text"  // ✅ Always show password
                                        className="inp-set"
                                        placeholder="Enter your new password"
                                        value={password}
                                        onChange={(e) => setPassword(e.target.value)}
                                        required
                                    />

                                    <label className='txt-lab txt-new'>Confirm Password</label>
                                    <input
                                        type="text"  // ✅ Always show password
                                        className="inp-set"
                                        placeholder="Re-enter your new password"
                                        value={confirmPassword}
                                        onChange={(e) => setConfirmPassword(e.target.value)}
                                        required
                                    />

                                    <button type="submit" className='mt-4 btn-sign'>Reset Password</button>

                                    <div className='box-end'>
                                        <p className='mt-2 mb-0 account-txt'>Remembered your password?</p>
                                        <a className='mb-0 mt-2 sign-txt link-line' href='/login'>Go to Login</a>
                                    </div>
                                </form>
                            </div>
                        </div>
                    </div>

                    <div className='col-6 box-back'>
                        <img className='vec-img' src='/images/onlyvector.png' alt="Background" />
                    </div>
                </div>
            </div>
        </section>
    );
}

export default ResetPassword;
