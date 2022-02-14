import "../css/auth.css"
import "react-pro-sidebar"
function Register() {
    // I type names in snake case because Django gets them and directly puts them in User model
    return (
        <div className={"auth-wrapper"}>
            <div className={"auth-inner"}>
                <form>
                    <h3>Sign Up</h3>
                    <div className="form-group">
                        <label>First name</label>
                        <input type="text" className="form-control" placeholder="First name" name={"first_name"}/>
                    </div>
                    <div className="form-group">
                        <label>Last name</label>
                        <input type="text" className="form-control" placeholder="Last name" name={"last_name"}/>
                    </div>
                    <div className="form-group">
                        <label>Email address</label>
                        <input type="email" className="form-control" placeholder="Enter email" name={"email"}/>
                    </div>
                    <div className="form-group">
                        <label>Password</label>
                        <input type="password" className="form-control" placeholder="Enter password" name={"password"}/>
                    </div>
                    <button type="submit" className="btn btn-primary btn-block">Sign Up</button>
                    <p className="forgot-password text-right">
                        Already registered <a href={"/login"}>sign in?</a>
                    </p>
                </form>
            </div>
        </div>
    );
}

export default Register