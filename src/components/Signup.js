import { useEffect, useState } from "react";
import { useLoader } from "./LoaderContext";
import 'bootstrap/dist/css/bootstrap.min.css';
import { useForm } from "react-hook-form";
import { Eye, EyeOff } from "lucide-react";
import { Link, useNavigate } from "react-router-dom";
import axios from "axios";

function Signup() {
    const navigate = useNavigate();
    const { register, handleSubmit, formState: { errors } } = useForm();
    const [showPassword, setShowPassword] = useState(false);
    const [error, setError] = useState("");
    const [message, setMessage] = useState("");
    const [emailVerified, setEmailVerified] = useState(false);

    const { setLoading } = useLoader();

    const AUTH_API_URL = process.env.REACT_APP_AUTH_API_URL;

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

    // ✅ Handle Signup Submission
const onSubmit = async (data) => {
    console.log("📤 Submitting signup form with data:", data);
    console.log("🔗 AUTH_API_URL:", AUTH_API_URL);  // Check if it's correctly loaded

    setError("");
    setMessage("");

    try {
        const response = await axios.post(`${AUTH_API_URL}/signup`, {
            username: data.name,
            email: data.email,
            password: data.password
        });

        console.log("✅ Server response:", response.data);  // Debug response

        if (response.data.status === "success") {
            setMessage("✅ Please check your inbox/spam. Email may take up to 2 minutes.");
        } else {
            setError("❌ " + response.data.message);
        }
    } catch (err) {
        console.error("❌ Signup error:", err);  // Show error in console
        setError("❌ " + (err.response?.data?.message || "Signup failed. Please try again."));
    }
};

    

    // ✅ Redirect to login **only if the email is verified**
    useEffect(() => {
        if (emailVerified) {
            setTimeout(() => navigate("/login"), 5000);
        }
    }, [emailVerified, navigate]);

    return (
    <section className="sec-signup">
        <div className="signup-form-wrapper">
            <div className="text-center mb-3">
                <img src="/images/Logo.png" alt="Logo" className="signup-logo" />
                <p className="wel-txt">Create an account</p>
            </div>

            {error && <p className="error-text">{error}</p>}
            {message && <p className="success-text">{message}</p>}

            <form className="form-space" onSubmit={handleSubmit(onSubmit)}>
                <label className="txt-lab">Full Name</label>
                <input
                    type="text"
                    className="inp-set"
                    placeholder="Enter your full name"
                    {...register("name", { required: "Full name is required" })}
                />
                {errors.name && <p className="error-text">{errors.name.message}</p>}

                <label className="txt-lab txt-new">Email</label>
                <input
                    type="email"
                    className="inp-set"
                    placeholder="Enter your email"
                    {...register("email", {
                        required: "Email is required",
                        pattern: {
                            value: /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/,
                            message: "Enter a valid email address"
                        }
                    })}
                />
                {errors.email && <p className="error-text">{errors.email.message}</p>}

                <label className="txt-lab txt-new">Password</label>
                <div className="relative">
                    <input
                        type={showPassword ? "text" : "password"}
                        className="inp-set"
                        placeholder="Enter your password"
                        {...register("password", {
                            required: "Password is required",
                            minLength: {
                                value: 6,
                                message: "Password must be at least 6 characters long"
                            }
                        })}
                    />
                    <button
                        type="button"
                        className="eye-toggle"
                        onClick={() => setShowPassword(!showPassword)}
                    >
                        {showPassword ? <EyeOff size={20} /> : <Eye size={20} />}
                    </button>
                </div>
                {errors.password && <p className="error-text">{errors.password.message}</p>}

                <button type="submit" className="mt-4 btn-sign">Sign up</button>

                <div className="box-end">
                    <p className="account-txt">Already have an account?</p>
                    <Link className="sign-txt link-line" to="/login">Login</Link>
                </div>
            </form>
        </div>
    </section>
);
}
// Log the AUTH_API_URL to verify it's set correctly

console.log("AUTH_API_URL:", process.env.REACT_APP_AUTH_API_URL);


export default Signup;
