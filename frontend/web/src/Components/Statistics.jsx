import styles from '../UserPages/Dashboard.module.css';
import { 
  Chart as ChartJS, 
  ArcElement, 
  Tooltip, 
  Legend, 
  CategoryScale, 
  LinearScale, 
  BarElement 
} from 'chart.js';
import { Bar } from 'react-chartjs-2';
import { useRef } from 'react';
import html2canvas from 'html2canvas';

const Statistcs = ({stats,chartData}) => {
    ChartJS.register(ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement);

    const printRef = useRef();

    const handleDownload = async () => {
        if (!printRef.current) return;

        try {
        const canvas = await html2canvas(printRef.current);
        const imageBase64 = canvas.toDataURL("image/png");
        const token = localStorage.getItem('userToken');
        const response = await fetch('http://127.0.0.1:8000/download/', {
            method: 'POST',
            headers: {
            'Content-Type': 'application/json',
            'Authorization': `Token ${token}`
            },
            body: JSON.stringify({
            chartImage: imageBase64,
            stats: stats,
            created_at: stats.created_at
            })
        });

        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `${stats.created_at}.pdf`;
            document.body.appendChild(a);
            a.click();
            a.remove();
        } else {
            alert("Download failed!");
        }

        } catch (error) {
        console.error("PDF Error:", error);
        }
    };

    return(
        <>
            <div ref={printRef}>
                <div className={styles.statsGrid}>
                    <div className={styles.statCard}>
                        <h4>Total Units</h4>
                        <div className={styles.statValue}>{stats.total_count}{console.log(stats.created_at)}</div>
                    </div>
                <div className={styles.statCard}>
                    <h4>Avg Pressure</h4>
                    <div className={styles.statValue}>{stats.averages.pressure} <span className={styles.unit}>bar</span></div>
                </div>
                <div className={styles.statCard}>
                    <h4>Avg Temp</h4>
                    <div className={styles.statValue}>{stats.averages.temperature} <span className={styles.unit}>°C</span></div>
                </div>
            </div>

            {chartData && (
                <div className={styles.chartContainer} style={{ height: '300px', marginTop: '2rem'}}>
                <h3>Equipment Distribution</h3>
                <Bar data={chartData} options={{ responsive: true, maintainAspectRatio: false,scales: 
                    {x:
                        {offset: true,    
                            grid: {
                                offset: true   
                            },
                            ticks: {
                                align: 'center',
                                autoSkip: false,
                                maxRotation: 0,
                                minRotation: 0,
                                font:{
                                size:10
                                }
                            }
                        } 
                    }
                    }} 
                />
                </div>
            )}
            </div>
            {chartData && <div style={{ display: 'flex', justifyContent: 'center', width: '100%' }}>
                <button onClick={handleDownload} className={styles.downloadBtn}>
                <svg 
                    width="18" height="18" viewBox="0 0 24 24" fill="none" 
                    stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"
                >
                    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
                    <polyline points="7 10 12 15 17 10" />
                    <line x1="12" y1="15" x2="12" y2="3" />
                </svg>
                Download Secured PDF
                </button>
            </div>}
        </>
    )
}

export default Statistcs