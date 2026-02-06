import LandingPage from "./LandingPage/LandingPage";
import Login from "./Authentication/Login";
import Signup from "./Authentication/Signup";
import Dashboard from "./UserPages/Dashboard";

import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import AppProvider from "./AppContext";

const App = () => {

    return (
        <AppProvider>
            <Router>
                <Routes>
                    <Route path="/" element={<LandingPage/>}/>
                    <Route path="/login" element={<Login/>}/>
                    <Route path="/signup" element={<Signup/>}/>
                    <Route path="/dashboard" element={<Dashboard/>}/>
                </Routes>
            </Router>
        </AppProvider>
    )
}

export default App;