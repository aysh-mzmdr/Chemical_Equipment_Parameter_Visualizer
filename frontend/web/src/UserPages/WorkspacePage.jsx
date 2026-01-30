import styles from './Dashboard.module.css';
import { 
  UploadCloud,
  ChevronRight,
} from 'lucide-react';

const WorkspacePage = () => {

  return(
    <div className={styles.workspace}>
      <div className={styles.uploadCard}>
        <div className={styles.uploadIconCircle}>
          <UploadCloud size={32} />
        </div>
        <h3>Upload Equipment Data</h3>
        <p>Drag and drop your CSV file here to begin analysis</p>
        <button className={styles.primaryBtn}>
          Select File <ChevronRight size={16} />
        </button>
      </div>
      
      {/* Placeholder for where graphs will go */}
      <div className={styles.statsGrid}>
        <div className={styles.statCard}></div>
        <div className={styles.statCard}></div>
        <div className={styles.statCard}></div>
      </div>
    </div>
  )
}

export default WorkspacePage