import { useState } from "react";
import { useForm } from "react-hook-form";
import { Eye, EyeOff } from "lucide-react";
import { Link, useNavigate } from "react-router-dom";
import axios from "axios";

function Login() {
    const navigate = useNavigate();
    const { register, handleSubmit, formState: { errors } } = useForm();
    const [showPassword, setShowPassword] = useState(false);
    const [error, setError] = useState("");

    const onSubmit = async (data) => {
        try {
            const response = await axios.post("http://127.0.0.1:5001/login", data);
            if (response.data.status === "success") {
                localStorage.setItem("user", JSON.stringify(response.data)); // Store user session
                localStorage.setItem("userId", response.data.user_id); // Store userId for chat history
                navigate('/Chat'); // Redirect after successful login
            }
        } catch (err) {
            setError("Invalid email or password.");
        }
    };

    return (
        <section className='sec-login'>
            <div className='container-fluid'>
                <div className='row height-row'>
                    <div className='col-6 col-top'>
                        <div className='d-flex justify-content-center'>
                            <div className='box-size'>
                                <div className='d-flex align-items-center box-pad'>
                                    <img className='inline-block' src='/images/we.png' alt="Logo" />
                                </div>
                                <p className='wel-txt'>Welcome back</p>
                                <p className='det-txt'>Please enter your details</p>

                                {error && <p className="error-text">{error}</p>}

                                <form className='form-space' onSubmit={handleSubmit(onSubmit)}>
                                    <label className='txt-lab'>Email address</label>
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

                                    <div className="relative">
                                        
                                        <div
                                            style={{
                                                position: "relative",  // ✅ Set relative position for parent container
                                                width: "100%",
                                            }}
                                        >
                                        <label className="txt-lab txt-new">Password</label>
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
                                            className="absolute right-2 top-1/2 transform -translate-y-1/2"
                                            onClick={() => setShowPassword(!showPassword)}
                                        >
                                            {showPassword ? <EyeOff size={20} /> : <Eye size={20} />}
                                        </button>
                                    </div>
                                    </div>
                                    {errors.password && <p className="error-text">{errors.password.message}</p>}

                                    <div className="d-flex justify-content-between mt-2">
                                        <div>
                                            <input className="form-check-input" type="checkbox" id="rememberMe" />
                                            <label className="form-check-label ml-2">Remember me</label>
                                        </div>
                                        <Link className='link-line' to='/forget'>
                                            Forgot password?
                                        </Link>
                                    </div>

                                    <button type="submit" className='mt-4 btn-sign'>Sign in</button>

                                    <p className='m-0 pt-2 pb-2 text-center'>Or</p>

                                    <button className='btn-sign btn-google' onClick={() => window.open('https://accounts.google.com/signup', '_blank')}>
                                        <img className='img-set' src='/images/google.png' alt="Google" />
                                        Sign in with Google
                                    </button>

                                    <div className='box-end'>
                                        <p className='mt-2 mr-2 mb-0 account-txt'>Don't have an account?</p>
                                        <Link className='mb-0 mt-2 sign-txt link-line' to='/signup'>Sign up</Link>
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

export default Login;
