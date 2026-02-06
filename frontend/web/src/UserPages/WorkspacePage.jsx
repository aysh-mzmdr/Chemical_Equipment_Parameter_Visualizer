import { useRef,useState } from 'react';
import styles from './Dashboard.module.css';
import { 
  UploadCloud,
  ChevronRight,
} from 'lucide-react';
import Statistics from "../Components/Statistics"

const WorkspacePage = () => {

  const token = localStorage.getItem('userToken')
  const fileInputRef = useRef(null);

  const handleBtnClick = () => {
  fileInputRef.current.click();
  };

  const [stats, setStats] = useState({total_count:0,averages:{pressure:0,temperature:0}});
  const [chartData, setChartData] = useState(null);

  const handleFileChange = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    if (file.type === "text/csv" || file.name.endsWith(".csv")) {
      console.log("CSV File Selected:", file.name);
    } 
    else {
      alert("Only CSV files are allowed.");
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://127.0.0.1:8000/upload/', {
        method: 'POST',
        headers:{
          "Authorization":`Token ${token}`
        },
        body: formData,
      });
      
      const data = await response.json();
      
      if (response.ok) {
        setStats(data);
        setChartData({
          labels: data.distribution.labels,
          datasets: [
            {
              label: 'Equipment Count',
              data: data.distribution.values,
              backgroundColor: [
                'rgba(56, 189, 248, 0.6)',
                'rgba(129, 140, 248, 0.6)',
                'rgba(244, 114, 182, 0.6)',
              ],
              borderColor: [
                'rgba(56, 189, 248, 1)',
                'rgba(129, 140, 248, 1)',
                'rgba(244, 114, 182, 1)',
              ],
              borderWidth: 1,
              barThickness:50
            },
          ],
        });
      }
    } 
    catch (error) {
      console.error("Upload failed", error);
    }
  };


  return(
    <div className={styles.workspace}>

      <div className={styles.uploadCard}>
        <div className={styles.uploadIconCircle}>
          <UploadCloud size={32} />
        </div>
        <h3>Upload Equipment Data</h3>
        <p>Drag and drop your CSV file here to begin analysis</p>
        
        <input 
          type="file" 
          ref={fileInputRef}
          onChange={handleFileChange}
          accept=".csv, application/vnd.ms-excel, text/csv"
          style={{ display: 'none' }} 
        />

        <button className={styles.primaryBtn} onClick={handleBtnClick}>
          Select File <ChevronRight size={16} />
        </button>
      </div>
      <div className={styles.historyCard} style={{paddingTop:"25px"}}>
        <Statistics 
          stats={stats} 
          chartData={chartData} 
        />
      </div>
      <p className={styles.securityNote}>
        🔒 <strong>Note:</strong> Downloaded file would be password protected. Use your <strong>email</strong> to open.
      </p>
    </div>
  )
}

export default WorkspacePage