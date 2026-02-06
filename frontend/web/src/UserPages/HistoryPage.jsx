import { useEffect, useState } from 'react';
import styles from './Dashboard.module.css';
import Statistics from '../Components/Statistics';

const HistoryPage = ({ title, icon }) => {
  const token = localStorage.getItem('userToken')

  const[info,setInfo]=useState(null)
  
  useEffect(() => {
      fetch('http://127.0.0.1:8000/record/',{headers:{'Authorization': `Token ${token}`}})
      .then(response => response.json())
      .then(data => setInfo(data.resultData))
      .catch(err => console.log(err))
  },[])

  return(
    <div className={styles.container} style={{display:"flex",flexWrap:"wrap",justifyContent:"center",gap:"250px"}}>
      {info && info.map((record, index) => {
        const formattedChartData = {
          labels: record.distribution.labels,
          datasets: [{
            label: 'Equipment Count',
            data: record.distribution.values,
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
              barThickness:50,
          }]
        };

        const formatDate = (isoString) => {
          const date = new Date(isoString);
          return {
            date: date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }),
            time: date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })
          };
        };
        const { date, time } = formatDate(record.created_at);
        return (
          <div key={index} className={styles.historyCard}>
            <h1 className={styles.indexBadge}>
              <span className={styles.dateText}>{date}</span>  
              <span className={styles.timeText}>{time}</span>
            </h1>
            <Statistics 
              stats={record} 
              chartData={formattedChartData} 
            />
          </div>
        );
      })}
    
    {(!info || info.length === 0) && <h1>No History</h1>}
  </div>
  )
}

export default HistoryPage
