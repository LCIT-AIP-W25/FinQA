import { useEffect } from "react";
import { useLoader } from "./LoaderContext"; // Import global loader

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


    const { setLoading } = useLoader();
    const AUTH_API_URL = process.env.REACT_APP_AUTH_API_URL || "http://127.0.0.1:5001";

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
        try {
            const response = await axios.post(`${AUTH_API_URL}/login`, data);
            if (response.data.status === "success") {
                localStorage.setItem("user", JSON.stringify(response.data)); // Store user session
                localStorage.setItem("userId", response.data.user_id); // Store userId for chat history
                localStorage.setItem("pdfChat_userId", response.data.user_id);
                
                // Clear any stale PDF info from old users
                localStorage.removeItem("pdfChat_filename");

                navigate('/home'); // Redirect after successful login
            }
        } catch (err) {
            setError("Invalid email or password.");
        }
    };

 return (
  <section className='sec-login'>
    <div className='d-flex justify-content-center align-items-center' style={{ width: '100%', minHeight: '100vh' }}>
      <div className='signup-form-wrapper'>
        <div className='text-center mb-3'>
          <img className='signup-logo' src='/images/Logo.png' alt="Logo" />
          <p className='wel-txt' style={{color: 'black'}}>Welcome back</p>
          <p className='det-txt'>Please enter your details</p>
        </div>

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

          <div className="relative" style={{ position: "relative", width: "100%" }}>
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
              className="eye-toggle"
              onClick={() => setShowPassword(!showPassword)}
            >
              {showPassword ? <EyeOff size={20} /> : <Eye size={20} />}
            </button>
          </div>
          {errors.password && <p className="error-text">{errors.password.message}</p>}

          <div className="d-flex justify-content-between mt-2">
            <div></div>
            <Link className='link-line' to='/forget'>Forgot password?</Link>
          </div>

          <button type="submit" className='mt-4 btn-sign'>Sign in</button>

          <div className='box-end'>
            <p className='mt-2 mr-2 mb-0 account-txt'>Don't have an account?</p>
            <Link className='mb-0 mt-2 sign-txt link-line' to='/signup'>Sign up</Link>
          </div>
        </form>
      </div>
    </div>
  </section>
);
}

export default Login;
