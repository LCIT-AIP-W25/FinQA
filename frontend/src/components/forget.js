import 'bootstrap/dist/css/bootstrap.min.css';
import { useState } from "react";
import { useForm } from "react-hook-form";
import { Link, useNavigate } from "react-router-dom";
import axios from "axios";

function ForgetPassword() {
    const navigate = useNavigate();
    const { register, handleSubmit, formState: { errors } } = useForm();
    const [message, setMessage] = useState("");

    const onSubmit = async (data) => {
        try {
            const response = await axios.post("http://127.0.0.1:5001/forget_password", data);
            if (response.data.status === "success") {
                setMessage("Reset link sent to your email.");
                navigate('/login');
            }
        } catch (err) {
            setMessage("Email not registered.");
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
                                <p className='det-txt'>Enter your email to reset your password</p>

                                {message && <p className="success-text">{message}</p>}

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
