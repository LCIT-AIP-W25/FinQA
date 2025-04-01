import 'bootstrap/dist/css/bootstrap.min.css';
import { useEffect } from "react";
import { useLoader } from "./LoaderContext";
import { useState } from "react";
import { useForm } from "react-hook-form";
import { Link } from "react-router-dom";
import axios from "axios";

function ForgetPassword() {
    const { register, handleSubmit, formState: { errors } } = useForm();
    const [message, setMessage] = useState("");
    const [error, setError] = useState("");
    const [resetLink, setResetLink] = useState(""); 

    const { setLoading } = useLoader();

    const AUTH_API_URL = "https://finqa-auth-app-ac1o.onrender.com";
    

    useEffect(() => {
    const requestInterceptor = axios.interceptors.request.use((config) => {
        setLoading(true);
        return config;
    });

    const responseInterceptor = axios.interceptors.response.use(
        (response) => {
        setLoading(false);
        return response;
        },
        (error) => {
        setLoading(false);
        return Promise.reject(error);
        }
    );

    return () => {
        axios.interceptors.request.eject(requestInterceptor);
        axios.interceptors.response.eject(responseInterceptor);
    };
    }, [setLoading]);

    const onSubmit = async (data) => {
        setMessage(""); 
        setError("");
    
        console.log("📩 Sending Forget Password Request:", data); 
    
        try {
            const response = await axios.post(`${AUTH_API_URL}/forget_password`, data);
            
            console.log("✅ Server Response:", response.data); 
            
            if (response.data.status === "success") {
                setMessage("✅ Password reset link sent to your email. Check your inbox & spam folder.");
            } else {
                setError("❌ " + (response.data.message || "Something went wrong."));
            }
        } catch (err) {
            console.error("❌ API Error:", err.response?.data); 
            setError("❌ Failed to send reset link. Try again.");
        }
    };
    
    

    return (
        <section className='sec-login'>
            <div className='container-fluid'>
                <div className='row height-row'>
                    <div className='col-6 col-top'>
                        <div className='d-flex justify-content-center'>
                            <div className='box-size'>
                                <p className='wel-txt'>Forgot Password</p>
                                <p className='det-txt'>Enter your email to receive a reset link.</p>

                                {message && <p className="success-text">{message}</p>}
                                {error && <p className="error-text">{error}</p>}

                                {/* ✅ Show Reset Link if available */}
                                {resetLink && (
                                    <div className="mt-3">
                                        <p className="info-text">Test Reset Link:</p>
                                        <a href={resetLink} target="_blank" rel="noopener noreferrer">{resetLink}</a>
                                    </div>
                                )}

                                <form className='form-space' onSubmit={handleSubmit(onSubmit)}>
                                    <label className='txt-lab'>Email</label>
                                    <input
                                        type="email"
                                        className='inp-set'
                                        placeholder='Enter your email'
                                        {...register("email", {
                                            required: "Email is required",
                                            pattern: {
                                                value: /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/,
                                                message: "Enter a valid email address"
                                            }
                                        })}
                                    />
                                    {errors.email && <p className="error-text">{errors.email.message}</p>}

                                    <button type="submit" className='mt-4 btn-sign'>Reset Password</button>

                                    <div className="mt-3">
                                        <Link className='mb-0 mt-2 sign-txt link-line' to='/login'>Back to Login</Link>
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

export default ForgetPassword;
