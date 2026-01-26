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
  
    // Apply theme to the website
  useEffect(() => {
       document.documentElement.setAttribute('data-theme', theme);
  }, [theme]);

  const [showPassword, setShowPassword] = useState(false);
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Login Attempt:', formData);
    // Add authentication logic here
  };

  const navigate=useNavigate();
  const toHome = () => {navigate("/")};
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

      {/* Main Login Card */}
      <div className={styles.loginCard}>
        
        {/* Header Section */}
        <div className={styles.header}>
          <div className={styles.logoBadge}>
            <FlaskConical size={28} className={styles.logoIcon} />
          </div>
          <h1 className={styles.title}>Welcome Back</h1>
          <p className={styles.subtitle}>
            Enter your credentials to access the equipment parameters dashboard.
          </p>
        </div>

        {/* Form Section */}
        <form onSubmit={handleSubmit} className={styles.form}>
          
          {/* Email Field */}
          <div className={styles.inputGroup}>
            <label htmlFor="email" className={styles.label}>Email</label>
            <div className={styles.inputWrapper}>
              <Mail className={styles.fieldIcon} size={18} />
              <input
                type="email"
                id="email"
                name="email"
                placeholder="example@company.com"
                value={formData.email}
                onChange={handleChange}
                className={styles.input}
                required
              />
            </div>
          </div>

          {/* Password Field */}
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
                value={formData.password}
                onChange={handleChange}
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

          {/* Submit Button */}
          <button type="submit" className={styles.submitBtn}>
            <span>Sign In</span>
            <ChevronRight size={18} />
          </button>
        </form>

        {/* Footer */}
        <div className={styles.footer}>
          <p>Don't have an account? <a href="#" className={styles.signupLink}>Sign up here</a></p>
        </div>
      </div>
    </div>
  );
};

export default Login;