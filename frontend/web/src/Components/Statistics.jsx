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

const Statistcs = ({stats,chartData}) => {
    ChartJS.register(ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement);

    return(
        <div>
        {/* Placeholder for where graphs will go */}
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

            {/* 2. Chart Section */}
            {chartData && (
                <div className={styles.chartContainer} style={{ height: '300px', marginTop: '2rem'}}>
                <h3>Equipment Distribution</h3>
                <Bar data={chartData} options={{ responsive: true, maintainAspectRatio: false,scales: 
                    {x:
                        {offset: true,      // Ensures the bar is centered directly on the label
                            grid: {
                                offset: true     // Ensures grid lines align with the offset
                            },
                            ticks: {
                                align: 'center',
                                autoSkip: false,
                                maxRotation: 0, // Forces horizontal text
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
    )
}

export default Statistcs