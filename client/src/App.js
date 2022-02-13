import 'bootstrap/dist/css/bootstrap.min.css';
import {Route, Routes} from "react-router-dom"
import Login from "./components/Login";
import Register from "./components/Register";

function App() {
    return (
        <div className="App">
            <div className={"auth-wrapper"}>
                <div className={"auth-inner"}>
                    <Routes>
                    <Route element={<Login/>} path={"/login"}/>
                    <Route element={<Register/>} path={"/register"}/>
                    </Routes>
                </div>
            </div>

        </div>
    );
}

export default App;
