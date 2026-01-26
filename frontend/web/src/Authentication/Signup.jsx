import { useState, useEffect,useContext } from 'react';
import styles from './Signup.module.css';
import { useNavigate } from 'react-router-dom';
import { AppContext } from '../AppContext';

import { 
  FlaskConical, 
  Mail, 
  Lock, 
  User,
  Eye, 
  EyeOff, 
  ArrowLeft,
  ChevronRight,
  Sun,
  Moon
} from 'lucide-react';

const Signup = () => {

  const {theme, setTheme} = useContext(AppContext);

  const toggleTheme = () => {
    setTheme((prev) => (prev === 'light' ? 'dark' : 'light'));
  };

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
  }, [theme]);
  
  
  // Form State
  const [showPassword, setShowPassword] = useState(false);
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    email: '',
    password: ''
  });

  // Form Handlers
  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Signup Attempt:', formData);
    // Add registration logic here
  };

  const navigate = useNavigate();
  const toHome = () => {navigate("/")}
  const toLogin = () => {navigate("/login")}

  return (
    <div className={styles.container}>
      {/* Back Navigation */}
      <div className={styles.backLink} style={{cursor:"pointer"}} onClick={toHome}>
        <ArrowLeft size={20} />
        <span>Home</span>
      </div>

      {/* Theme Toggle */}
      <button className={styles.themeToggle} onClick={toggleTheme} aria-label="Toggle Theme">
        {theme === 'light' ? <Moon size={20} /> : <Sun size={20} />}
      </button>

      {/* Signup Card */}
      <div className={styles.signupCard}>
        <div className={styles.header}>
          <div className={styles.logoBadge}>
            <FlaskConical size={28} className={styles.logoIcon} />
          </div>
          <h1 className={styles.title}>Create Account</h1>
          <p className={styles.subtitle}>
            Join the platform to visualize and analyze your chemical equipment parameters.
          </p>
        </div>

        <form onSubmit={handleSubmit} className={styles.form}>
          
          <div className={styles.row}>
            <div className={styles.inputGroup}>
              <label htmlFor="firstName" className={styles.label}>First Name</label>
              <div className={styles.inputWrapper}>
                <User className={styles.fieldIcon} size={18} />
                <input
                  type="text"
                  id="firstName"
                  name="firstName"
                  placeholder="John"
                  value={formData.firstName}
                  onChange={handleChange}
                  className={styles.input}
                  required
                />
              </div>
            </div>

            <div className={styles.inputGroup}>
              <label htmlFor="lastName" className={styles.label}>Last Name</label>
              <div className={styles.inputWrapper}>
                <input
                  type="text"
                  id="lastName"
                  name="lastName"
                  placeholder="Doe"
                  value={formData.lastName}
                  onChange={handleChange}
                  className={styles.input}
                  style={{ paddingLeft: '1rem' }}
                  required
                />
              </div>
            </div>
          </div>

          <div className={styles.inputGroup}>
            <label htmlFor="email" className={styles.label}>Work Email</label>
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

          <div className={styles.inputGroup}>
            <label htmlFor="password" className={styles.label}>Password</label>
            <div className={styles.inputWrapper}>
              <Lock className={styles.fieldIcon} size={18} />
              <input
                type={showPassword ? "text" : "password"}
                id="password"
                name="password"
                placeholder="Create a strong password"
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

          <div className={styles.inputGroup}>
            <label htmlFor="password" className={styles.label}>Confirm Password</label>
            <div className={styles.inputWrapper}>
              <Lock className={styles.fieldIcon} size={18} />
              <input
                type={showPassword ? "text" : "password"}
                id="password"
                name="password"
                placeholder="Rewrite your password"
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

          <button type="submit" className={styles.submitBtn}>
            <span>Get Started</span>
            <ChevronRight size={18} />
          </button>
        </form>

        <div className={styles.footer}>
          <p>Already have an account? <span className={styles.link} style={{cursor:"pointer"}} onClick={toLogin}>Log In</span></p>
        </div>
      </div>
    </div>
  );
};

export default Signup;