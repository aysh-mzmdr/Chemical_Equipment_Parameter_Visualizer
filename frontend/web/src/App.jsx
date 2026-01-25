import { useState, useEffect } from 'react';
import styles from './App.module.css';
import { 
  UploadCloud, 
  BarChart3, 
  Sun, 
  Moon, 
  FlaskConical, 
  ArrowRight,
  Database,
  FileText
} from 'lucide-react';

const App = () => {
  const [theme, setTheme] = useState('dark');

  const toggleTheme = () => {
    setTheme((prev) => (prev === 'light' ? 'dark' : 'light'));
  };

  // Apply theme to the website
  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
  }, [theme]);

  return (
    <div className={styles.container}>

      {/* Navbar*/}
      <nav className={styles.navbar}>
        <div className={styles.logo}>
          <FlaskConical className={styles.logoIcon} />
          <span>Chemical Equipment<span className={styles.highlight}> Parameter Visualizer</span></span>
        </div>
        <div className={styles.navActions}>
          <button className={styles.themeToggle} onClick={toggleTheme}>
            {theme === 'light' ? <Moon size={20} /> : <Sun size={20} />}
          </button>
          
          <button className={styles.loginBtn}><span>Login</span></button>
          <button className={styles.downloadBtn}>Download App</button>
          <button className={styles.signupBtn}>Sign-Up</button>
        </div>
      </nav>

      {/* Hero Section */}
      <header className={styles.hero}>
        <div className={styles.heroContent}>
          <h1 className={styles.title}>
            Visualize Chemical <br />
            <span className={styles.textGradient}>Equipment Parameters</span>
          </h1>
          <p className={styles.subtitle}>
            Transform CSV files into interactive, real-time statistical charts. 
            Designed for chemical engineers to monitor pressure, temperature, 
            and flow rates with precision.
          </p>
          
          <div className={styles.ctaGroup}>
            <button className={styles.ctaUpload}>
              <UploadCloud size={20} />
              <span>Upload CSV Data</span>
            </button>
            <button className={styles.ctaDemo}>
              View Live Demo <ArrowRight size={18} />
            </button>
          </div>
        </div>
  
        {/* Mock Graph */}
        <div className={styles.heroVisual}>
          <div className={styles.monitorCard}>
            
            {/* Monitor Head */}
            <div className={styles.monitorHeader}>
              <div className={styles.windowControls}>
                <div className={styles.controlDot} style={{background:'#ada8a7'}}></div>
                <div className={styles.controlDot} style={{background:'#ada8a7'}}></div>
                <div className={styles.controlDot} style={{background:'#ada8a7'}}></div>
              </div>
            </div>

            {/* Monitor Body */}
            <div className={styles.monitorBody}>

              {/* Left: Practical Bar Graph */}
              <div className={styles.chartSection}>
                <div className={styles.chartHeader}>
                  <span className={styles.chartLabel}>Equipment Count by Type</span>
                </div>
                
                <div className={styles.graphContainer}>
                  {/* Background Grid Lines */}
                  <div className={styles.gridLayer}>
                    <div className={styles.gridLine}></div>
                    <div className={styles.gridLine}></div>
                    <div className={styles.gridLine}></div>
                    <div className={styles.gridLine}></div>
                  </div>

                  {/* Bars Container */}
                  <div className={styles.barsLayer}>
                    
                    {/* Bar 1: Reactors */}
                    <div className={styles.barColumn}>
                      
                      <div className={styles.barVisual} style={{height: '80%'}}></div>
                      <span className={styles.barLabel}>Reactors</span>
                    </div>

                    {/* Bar 2: Tanks */}
                    <div className={styles.barColumn}>
                      
                      <div className={styles.barVisual} style={{height: '45%'}}></div>
                      <span className={styles.barLabel}>Tanks</span>
                    </div>

                    {/* Bar 3: Heat Exchangers */}
                    <div className={styles.barColumn}>
                      
                      <div className={styles.barVisual} style={{height: '60%'}}></div>
                      <span className={styles.barLabel}>Heat Exchangers</span>
                    </div>

                    {/* Bar 4: Pumps */}
                    <div className={styles.barColumn}>
                      
                      <div className={styles.barVisual} style={{height: '30%'}}></div>
                      <span className={styles.barLabel}>Pumps</span>
                    </div>

                  </div>
                </div>
              </div>

              {/* Right: Parameter Grid */}
              <div className={styles.paramGrid}>
                <div className={styles.paramBox}>
                  <span className={styles.pLabel}>Average Reactor Pressure</span>
                  <span className={styles.pValue}>24.5 Bar</span>
                </div>
                <div className={styles.paramBox}>
                  <span className={styles.pLabel}>Average Flow Rate</span>
                  <span className={styles.pValue}>120 L/min</span>
                </div>
                <div className={styles.paramBox}>
                  <span className={styles.pLabel}>Status</span>
                  <span className={styles.pBadge}>GOOD</span>
                </div>
              </div>

            </div>
          </div>
        </div>
      </header>

      {/* Features Grid */}
      <section className={styles.features}>
        <div className={styles.featureCard}>
          <div className={styles.iconBox}><Database size={24} /></div>
          <h3>Instant Parsing</h3>
          <p>Upload your equipment CSV files. We handle the parsing logic instantly via our secure API.</p>
        </div>
        <div className={styles.featureCard}>
          <div className={styles.iconBox}><BarChart3 size={24} /></div>
          <h3>Statistical Visualization</h3>
          <p>Auto-generated histograms, scatter plots, and heatmaps tailored for process engineering data.</p>
        </div>
        {/* COMBINED: History & PDF Reports */}
        <div className={styles.featureCard}>
          <div className={styles.iconBox}><FileText size={24} /></div>
          <h3>History & Reports</h3>
          <p>Automatically store your last 5 datasets for trend review and generate professional PDF reports with statistical summaries.</p>
        </div>
      </section>
    </div>
  );
};

export default App;