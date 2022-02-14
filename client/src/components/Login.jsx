import "../css/auth.css"
import Api from "../api/Api"


function Login() {

    async function onClick(form) {
        const f = new FormData(form)
        const body = [...f.entries()].reduce((acc, [k, v]) => Object.assign(acc, {
            [k]: v
        }), {})
        await Api().generateRequest("", "post", body, "application/json")
        //redirect or populate form with errors
    }
    return (
        <div className={"auth-wrapper"}>
            <div className={"auth-inner"}>
                <form className={"custom-form"}>
                    <h3>Sign In</h3>
                    <div className="form-group">
                        <label>Email address</label>
                        <input type="email" className="form-control" placeholder="Enter email"/>
                    </div>
                    <div className="form-group">
                        <label>Password</label>
                        <input type="password" className="form-control" placeholder="Enter password"/>
                    </div>
                    <div className="form-group">
                        <div className="custom-control custom-checkbox">
                            <input type="checkbox" className="custom-control-input" id="customCheck1"/>
                            <label className="custom-control-label" htmlFor="customCheck1">Remember me</label>
                        </div>
                    </div>
                    <button onClick={onClick} type="submit" className="btn btn-primary btn-block">Submit</button>
                    <p className="forgot-password text-right">
                        Forgot <a href="#">password?</a>
                    </p>
                </form>
            </div>
        </div>
    );
}


export default Login

