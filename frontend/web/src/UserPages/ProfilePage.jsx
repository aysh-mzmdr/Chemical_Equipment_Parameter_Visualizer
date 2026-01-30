import styles from './Dashboard.module.css';

const ProfilePage = ({ title, icon }) => {

  return(
    <div className={styles.placeholderState}>
      <div className={styles.placeholderIcon}>{icon}</div>
      <h3>{title}</h3>
      <p>This module is currently under development.</p>
    </div>
  )
}

export default ProfilePage
