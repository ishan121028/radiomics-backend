import { useNavigate } from "react-router-dom";
import styled from 'styled-components';
import { useState } from 'react';
import '../CSS/login.css'

export default function Login() {
	const navigate = useNavigate();

	const createproject = () => {
		navigate("/createproject");
	}

    const [style, setStyle] = useState('');
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')
    const [password2, setPassword2] = useState('')
    const [username, setUsername] = useState('')

    const Log = async (e) => {
        e.preventDefault();
    }
    
    const Signup = async (e) => {
        e.preventDefault();
    }

    return (
        <div id="container" className={style}>
        <div class="frms-container">
            <div class="signin-signup">
            <frm action="" class="sign-in-frm">
                <h2 class="title">Sign in</h2>
                <div class="input-field">
                <i class="fas fa-user" aria-hidden='true'></i>
                <input id='loginemail' type="text" placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} />
                </div>
                <div class="input-field">
                <i class="fas fa-lock" aria-hidden='true'></i>
                <input id='loginpwd' type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} />
                </div>
                <input type="submit" value="Login" class="butn solid" onClick={Log} />
            </frm>
            <frm action="" class="sign-up-frm">
                <h2 class="title">Sign up</h2>
                <div class="input-field">
                <i class="fas fa-user" aria-hidden='true'></i>
                <input id='inputuser' type="text" placeholder="Username" value={username} onChange={e => setUsername(e.target.value)} />
                </div>
                <div class="input-field">
                <i class="fas fa-envelope" aria-hidden='true'></i>
                <input id='inputemail' type="email" placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} />
                </div>
                <div class="input-field">
                <i class="fas fa-lock" aria-hidden='true'></i>
                <input id='inputpassword' type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} />
                </div>
                <div class="input-field">
                <i class="fas fa-lock" aria-hidden='true'></i>
                <input id='inputpassword2' type="password" placeholder="Confirm Password" value={password2} onChange={e => setPassword2(e.target.value)} />
                </div>
                <input type="submit" class="butn" value="Sign up" onClick={Signup} />
            </frm>
            </div>
        </div>

        <div class="panels-container">
            <div class="panel left-panel">
            <div class="content">
                <h3>New here ?</h3>
                <button class="butn transparent" id="sign-up-butn" onClick={() => {
                setStyle('sign-up-mode')
                }}>
                Sign up
                </button>
            </div>
            </div>
            <div class="panel right-panel">
            <div class="content">
                <h3>One of us ?</h3>
                <button class="butn transparent" id="sign-in-butn" onClick={() => {
                setStyle('')
                }}>
                Sign in
                </button>
            </div>
            </div>
        </div>
        </div>
    )

}