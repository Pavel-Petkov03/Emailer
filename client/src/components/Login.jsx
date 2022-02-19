import "../css/auth.css"
import {useNavigate} from "react-router-dom"
import {onClick} from "../utils/initialSubmitCall.js";
import {endpoints} from "../api/endpoints";

function Login() {
    const router = useNavigate()

    return (
        <div className={"auth-wrapper"}>
            <div className={"auth-inner"}>
                <form className={"custom-form"}>
                    <h3>Sign In</h3>
                    <div className="form-group">
                        <label>Email address</label>
                        <input type="email" className="form-control" placeholder="Enter email" name={"username"}/>
                    </div>
                    <div className="form-group">
                        <label>Password</label>
                        <input type="password" className="form-control" placeholder="Enter password" name={"password"}/>
                    </div>
                    <button onClick={onClick.bind(this, endpoints.login, router)} type="submit"
                            className="btn btn-primary btn-block">Submit
                    </button>
                    <p className="forgot-password text-right">
                        Forgot <a href="#">password?</a>
                    </p>
                </form>
            </div>
        </div>
    );
}

export default Login

