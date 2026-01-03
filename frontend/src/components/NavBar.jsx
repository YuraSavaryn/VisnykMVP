import React from 'react';
import styles from './Navbar.module.css';

const Navbar = ({ activeTab, setActiveTab }) => {
  return (
    <div className={styles.navbar}>
      <div className={styles.navbarContainer}>
        <button 
          className={`${styles.navLink} ${activeTab === 'fresh' ? styles.active : ''}`}
          onClick={() => setActiveTab('fresh')}
        >
          Свіжі новини
        </button>
        <button 
          className={`${styles.navLink} ${activeTab === 'important' ? styles.active : ''}`}
          onClick={() => setActiveTab('important')}
        >
          Важливі новини
        </button>
        <button 
          className={`${styles.navLink} ${activeTab === 'agent' ? styles.active : ''}`}
          onClick={() => setActiveTab('agent')}
        >
          Вісник (AI)
        </button>
      </div>
    </div>
  );
};

export default Navbar;