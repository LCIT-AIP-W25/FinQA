import 'bootstrap/dist/css/bootstrap.min.css';
import { useState } from "react";
import { useForm } from "react-hook-form";
import { Link, useNavigate } from "react-router-dom";

function ForgetPassword() {
    const navigate = useNavigate();
    const { register, handleSubmit, formState: { errors } } = useForm();

    const onSubmit = (data) => {
        console.log(data);
        // Add API call or logic to handle password reset
        navigate('/login');
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
                                <p className='wel-txt'>Forget Password</p>
                                <p className='det-txt'>Please enter your email</p>

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

                                    <button type="submit" className='mt-4 btn-sign'>Forget Password</button>

                                    <p className='m-0 pt-2 pb-2 text-center'>Or</p>

                                    <div className='box-end'>
                                        <p className='mt-2 mr-2 mb-0 account-txt'>Don't have an account?</p>
                                        <Link className='mb-0 mt-2 sign-txt link-line' to='/signup'>Sign up</Link>
                                    </div>
                                </form>
                            </div>
                        </div>
                    </div>
                    <div className='col-6 box-back'>
                        <div>
                            <img className='vec-img' src='/images/onlyvector.png' alt="Background" />
                        </div>
                    </div>
                </div>
            </div>
        </section>
    );
}

export default ForgetPassword;
