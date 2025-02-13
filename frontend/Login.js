function Login() {
    return (

        <>

            <section className='sec-login'>
                <div className='container'>

                    <div className='row height-row'>

                        <div className='col-6 col-top'>

                            <div className='d-flex justify-content-center'>
                                <div className='box-size'>

                                    <div className='d-flex align-items-center box-pad'>
                                        <img className='inline-block' src='/images/we.png'></img>

                                    </div>



                                    <p className='wel-txt'>
                                        Welcome back

                                    </p>
                                    <p className='det-txt'>
                                        Please enter your details
                                    </p>

                                    <form className='form-space'>

                                        <label className='txt-lab'>
                                            Email address
                                        </label>

                                        <input className='inp-set' placeholder='Enter your email'>

                                        </input>

                                        <label className='txt-lab txt-new'>
                                            Password
                                        </label>

                                        <input className='inp-set' placeholder='Enter your password'>

                                        </input>

                                        <div className="form-check check-dev mt-2 d-flex">
                                            <div>


                                                <input className="form-check-input" type="checkbox" id="flexCheckDefault" />
                                                <label className="form-check-label ml-2 check-txt" htmlFor="flexCheckDefault">
                                                    Remember for 30 days
                                                </label>    </div> <div>
                                                <a className='link-line' to="/">

                                                    Forget password

                                                </a></div>


                                        </div>

                                        <button className='mt-4 btn-sign'>

                                            Sign in
                                        </button>

                                        <p className='m-0 pt-2 pb-2 text-center'>Or</p>

<button className=' btn-sign btn-google'>
    <img className='img-set' src='/images/google.png'></img>
    Sign up with google
</button>
{/* other sign in buttons */}
{/*
 <button className='mt-2 btn-sign btn-google'>
    <img className='img-set' src='/images/microsoft.png'></img>
    Sign up with microsoft
</button>

<button className='mt-2 btn-sign btn-google'>
    <img className='img-set' src='/images/apple-logo.png'></img>
    Sign up with apple
</button>  */}
{/* other sign in buttons */}
<div className='d-flex w-100 justify-content-center mt-4 mb-4'>

    <button className=' btn-ntr'>
        <img className='img-set demo-icon' src='/images/apple-logo.png'></img>
    </button>
    <button className=' btn-ntr'>
        <img className='img-set demo-icon' src='/images/google.png'></img>
        </button>
        
    <button className='btn-ntr'>

        <img className='img-set' src='/images/microsoft.png'></img>
    </button>

</div>




                                

                                        <div className='box-end'>
                                            <p className='mt-2 mr-2 mb-0 account-txt'>
                                                Don't have an account?


                                            </p>
                                            <a className='mb-0 mt-2 sign-txt link-line' href=''>
                                                Sign up
                                            </a>

                                        </div>



                                    </form>





                                </div>

                            </div>




                        </div>

                        <div className='col-6 box-back'>

                            <div>
                                <img className='vec-img' src='/images/onlyvector.png'></img>

                            </div>

                        </div>

                    </div>



                </div>
            </section>


        </>


    );
}

export default Login;
