import "../css/auth.css"
import Api from "../api/Api"
import {useNavigate} from "react-router-dom"
import {endpoints} from "../api/endpoints"
function Login() {
    const router = useNavigate()
    async function onClick(ev) {
        ev.preventDefault()
        console.log(1)
        const body = getDataFromForm(document.querySelector("form"))
        let api = new Api()
        api.generateRequest(endpoints.login, "post", body, "application/json").catch(er => {
            console.log(er)
        }).then(data => {
            router("/")
        })
    }

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
                    <button onClick={(ev) => onClick(ev)} type="submit" className="btn btn-primary btn-block">Submit</button>
                    <p className="forgot-password text-right">
                        Forgot <a href="#">password?</a>
                    </p>
                </form>
            </div>
        </div>
    );
}
function getDataFromForm(form){
    let formData = new FormData(form)
    return [...formData].reduce((acc , [k , v]) => Object.assign(acc , {[k] : v}), {})
}

export default Login

