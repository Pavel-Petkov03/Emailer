import 'bootstrap/dist/css/bootstrap.min.css';
import {Route, Routes} from "react-router-dom"
import Login from "./components/Login";
import Register from "./components/Register";
import SideNav from "./components/SideNav";

function App() {
    return (
        <div className="App">
            <SideNav />
            <Routes>
                <Route element={<Login/>} path={"/login"}/>
                <Route element={<Register/>} path={"/register"}/>
            </Routes>

        </div>
    );
}

export default App;
