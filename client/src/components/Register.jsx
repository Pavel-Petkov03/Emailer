import "../css/auth.css"
import "react-pro-sidebar"
import {useNavigate} from "react-router-dom"
import Api from "../api/Api";
import {retrieveFormData} from "../utils/retrieveFormData.js"
function Register() {
    const router = useNavigate()

    function onSubmit() {
        let body = retrieveFormData(document.querySelector("form"))
        let api = new Api("/login")
        api.apiCall("post", body, "application/json").then(data => {
            router("/")
        }).catch(er => {
            // toggle modal
        })
    }

    return (
        <div className={"auth-wrapper"}>
            <div className={"auth-inner"}>
                <form>
                    <h3>Sign Up</h3>
                    <div className="form-group">
                        <label>Username</label>
                        <input type="text" className="form-control" placeholder="Last name" name={"username"}/>
                    </div>
                    <div className="form-group">
                        <label>Email address</label>
                        <input type="email" className="form-control" placeholder="Enter email" name={"email"}/>
                    </div>
                    <div className="form-group">
                        <label>Password</label>
                        <input type="password" className="form-control" placeholder="Enter password" name={"password"}/>
                    </div>
                    <button type="submit" className="btn btn-primary btn-block" onClick={(ev) => {
                        ev.preventDefault()
                        console.log(formState)
                    }}>Sign Up
                    </button>
                    <p className="forgot-password text-right">
                        Already registered <a href={"/login"}>sign in?</a>
                    </p>
                </form>
            </div>
        </div>
    );
}



export default Register