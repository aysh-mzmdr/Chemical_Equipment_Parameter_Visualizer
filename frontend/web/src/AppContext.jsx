import { createContext,useState } from "react";

export const AppContext = createContext();

const AppProvider = ({children}) => {

    const[theme,setTheme]=useState("dark");

    return (
        <AppContext.Provider value={{theme,setTheme}}>
            {children}
        </AppContext.Provider>
    )
}

export default AppProvider;