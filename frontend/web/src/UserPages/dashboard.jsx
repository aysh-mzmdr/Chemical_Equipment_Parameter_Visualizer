import ProfilePage from "./ProfilePage"
import HistoryPage from "./HistoryPage"
import WorkspacePage from "./WorkspacePage"
import { AppContext } from "../AppContext";
import { useState, useEffect, useContext} from 'react';
import styles from './Dashboard.module.css';
import { useNavigate } from 'react-router-dom';
import { 
  FlaskConical, 
  LayoutDashboard, 
  History, 
  UserCircle, 
  LogOut, 
  Sun, 
  Moon,
  Menu,
  X
} from 'lucide-react';

const Dashboard = () => {

    const [isSidebarOpen, setIsSidebarOpen] = useState(window.innerWidth > 768);
    const [activeTab, setActiveTab] = useState('Dashboard');

    const {theme,setTheme} = useContext(AppContext)
    
      const toggleTheme = () => {
        setTheme((prev) => (prev === 'light' ? 'dark' : 'light'));
      };
    
      useEffect(() => {
        document.documentElement.setAttribute('data-theme', theme);
      }, [theme]);


    useEffect(() => {
        const handleResize = () => {
        if (window.innerWidth <= 768) setIsSidebarOpen(false);
        else setIsSidebarOpen(true);
        };
        window.addEventListener('resize', handleResize);
        return () => window.removeEventListener('resize', handleResize);
    }, []);

    const toggleSidebar = () => setIsSidebarOpen(!isSidebarOpen);
    const user=JSON.parse(localStorage.getItem("userData"))
    const navigate = useNavigate();

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

    const renderContent = () => {
        switch (activeTab) {
        case 'Dashboard':
            return <WorkspacePage/>;
        case 'History':
            return <HistoryPage/>;
        case 'Profile':
            return <ProfilePage/>;
        default:
            return <WorkspacePage />;
        }
    };

    return (
        <div className={styles.container}>

        <aside className={`${styles.sidebar} ${isSidebarOpen ? styles.open : styles.closed}`}>
        
        {/* Mobile Only: Close Button inside Sidebar */}
        <button className={styles.mobileCloseBtn} onClick={toggleSidebar}>
          <X size={24} />
        </button>

        <div className={styles.logoSection}>
            <div className={styles.logoIconBox}>
                <FlaskConical size={24} />
            </div>
            <span className={styles.logoText}>Chemical Equipment<br></br><span className={styles.highlight}> Parameter Visualizer</span></span>
        </div>

        <nav className={styles.navMenu}>
        <button 
            className={`${styles.navItem} ${activeTab === 'Dashboard' ? styles.active : ''}`}
            onClick={() => setActiveTab('Dashboard')}
        >
            <LayoutDashboard size={20} />
            <span>Workspace</span>
            {activeTab === 'Dashboard' && <div className={styles.activeIndicator} />}
        </button>

        <button 
            className={`${styles.navItem} ${activeTab === 'History' ? styles.active : ''}`}
            onClick={() => setActiveTab('History')}
        >
            <History size={20} />
            <span>History</span>
            {activeTab === 'History' && <div className={styles.activeIndicator} />}
        </button>

        <button 
            className={`${styles.navItem} ${activeTab === 'Profile' ? styles.active : ''}`}
            onClick={() => setActiveTab('Profile')}
        >
            <UserCircle size={20} />
            <span>Profile</span>
            {activeTab === 'Profile' && <div className={styles.activeIndicator} />}
        </button>
        </nav>

        <div className={styles.sidebarFooter}>
        <div className={styles.divider} />
        
        <button className={styles.footerItem} onClick={toggleTheme}>
            {theme === 'light' ? <Moon size={20} /> : <Sun size={20} />}
            <span>{theme === 'light' ? 'Dark Mode' : 'Light Mode'}</span>
        </button>

        <button className={`${styles.footerItem} ${styles.logoutBtn}`} onClick={handleLogout}>
            <LogOut size={20} />
            <span>Logout</span>
        </button>

        <div className={styles.userMiniProfile}>
            <div className={styles.userAvatar}>{user.first_name[0]}{user.last_name[0]}</div>
            <div className={styles.userInfo}>
            <span className={styles.userName}>{user.first_name} {user.last_name}</span>
            <span className={styles.userRole}>{user.role}</span>
            </div>
        </div>
        </div>
        
      </aside>
      
      {/* Mobile Overlay (Click outside to close) */}
      {isSidebarOpen && <div className={styles.mobileOverlay} onClick={() => setIsSidebarOpen(false)} />}

      {/* Main Content */}
       <main className={styles.mainContent} style={{ marginLeft: !isSidebarOpen ? '0px' : '260px' }}
>
            <header className={styles.topHeader}>
                <button className={styles.hamburgerBtn} onClick={toggleSidebar}>
                    <Menu size={24} />
                </button>
                <h2 className={styles.pageTitle}>
                    {activeTab}
                </h2>
            </header>

            <div className={styles.contentWrapper}>
                {renderContent()}
            </div>
        </main>
    </div>
    );
};

export default Dashboard;