import LandingPage from "./LandingPage/LandingPage";
import Login from "./Authentication/Login";

import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import AppProvider from "./AppContext";

const App = () => {

    return (
        <AppProvider>
            <Router>
                <Routes>
                    <Route path="/" element={<LandingPage/>}/>
                    <Route path="/login" element={<Login/>}/>
                </Routes>
            </Router>
        </AppProvider>
    )
}

export default App;