
const dashboard = () => {

    const handleLogout = async() => {
        const token = localStorage.getItem("userToken")
        try{
            if(!token){
                navigate("/")
            }
            const response = await fetch(`http://127.0.0.1:8000/logout/`,{
                method:"POST",
                headers:{
                    'Authorization': `Token ${token}`,
                    'Content-type': 'application/json'
                }
            })
            if(response.status===200){
                localStorage.removeItem("userToken")
                localStorage.removeItem("userData")
                navigate("/")
            }
        }
        catch(err){
            console.log(err)
        }
    }

    return(
        <button onClick={handleLogout}>logout</button>
    )
}

export default dashboard;