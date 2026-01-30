import { useState,useContext,useEffect } from 'react';
import styles from './Login.module.css';
import { AppContext } from '../AppContext';
import { useNavigate } from 'react-router-dom';
import { 
  FlaskConical, 
  Mail, 
  Lock, 
  Eye, 
  EyeOff, 
  ArrowLeft,
  ChevronRight,
  Sun,
  Moon
} from 'lucide-react';

const Login = () => {
  const {theme,setTheme} = useContext(AppContext)

  const toggleTheme = () => {
      setTheme((prev) => (prev === 'light' ? 'dark' : 'light'));
  };
  
  useEffect(() => {
       document.documentElement.setAttribute('data-theme', theme);
  }, [theme]);

  const[showPassword,setShowPassword] = useState("");

  const[email,setEmail] = useState("");
  const[password,setPassword] = useState("");

  const handleLogin = async(e) => {
    e.preventDefault()
    try{
      const response=await fetch(`http://127.0.0.1:8000/login/`,{
          method:"POST",
          credentials:"include",
          headers:{
            "Content-type":"application/json"
          },
          body:JSON.stringify({
            username:email,
            password:password,
          })
      })
      if(response.status===200){
        const data = await response.json()
        localStorage.setItem('userToken',data.token)
        localStorage.setItem('userData',JSON.stringify(data.user))
        navigate("/dashboard");
      }
      else
        throw new Error("Invalid Creadentials")
    }
    catch(err){
      console.log(err)
    }

  }

  const navigate=useNavigate();
  const toHome = () => {navigate("/")};
  const toSignup = () => {navigate("/signup")}
  return (
    <div className={styles.container}>
        <button className={styles.themeToggle} onClick={toggleTheme}>
            {theme === 'light' ? <Moon size={20} /> : <Sun size={20} />}
        </button>
      {/* Back Navigation */}
      <div className={styles.backLink} onClick={toHome} style={{cursor:"pointer"}}>
        <ArrowLeft size={20} />
        <span>Home</span>
      </div>

      {/* Login Card */}
      <div className={styles.loginCard}>
        <div className={styles.header}>
          <div className={styles.logoBadge}>
            <FlaskConical size={28} className={styles.logoIcon} />
          </div>
          <h1 className={styles.title}>Welcome Back</h1>
          <p className={styles.subtitle}>
            Enter your credentials to access the equipment parameters dashboard.
          </p>
        </div>

        <form onSubmit={handleLogin} className={styles.form}>
          
          <div className={styles.inputGroup}>
            <label htmlFor="email" className={styles.label}>Email</label>
            <div className={styles.inputWrapper}>
              <Mail className={styles.fieldIcon} size={18} />
              <input
                type="email"
                id="email"
                name="email"
                placeholder="example@company.com"
                onChange={e => setEmail(e.target.value)}
                className={styles.input}
                required
              />
            </div>
          </div>

          <div className={styles.inputGroup}>
            <div className={styles.labelRow}>
              <label htmlFor="password" className={styles.label}>Password</label>
              <a href="#" className={styles.forgotLink}>Forgot password?</a>
            </div>
            <div className={styles.inputWrapper}>
              <Lock className={styles.fieldIcon} size={18} />
              <input
                type={showPassword ? "text" : "password"}
                id="password"
                name="password"
                placeholder="Enter your password"
                onChange={e => setPassword(e.target.value)}
                className={styles.input}
                required
              />
              <button 
                type="button" 
                className={styles.eyeBtn}
                onClick={() => setShowPassword(!showPassword)}
              >
                {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
              </button>
            </div>
          </div>

          <button type="submit" className={styles.submitBtn}>
            <span>Sign In</span>
            <ChevronRight size={18} />
          </button>
        </form>

       <div className={styles.footer}>
          <p>Don't have an account? <span className={styles.signupLink} style={{cursor:"pointer"}} onClick={toSignup}>Sign up here</span></p>
        </div>
      </div>
    </div>
  );
};

export default Login;