import React from 'react';
import styles from './Header.module.css';
import pigeonLogo from '../assets/pigeon_logo_edit.jpg'; 

const Header = () => {
  return (
    <header className={styles.header}>
      <div className={styles.container}>
        
        <div className={styles.leftSection}>
          <img 
            src={pigeonLogo} 
            alt="Pigeon Logo" 
            className={styles.pigeonImage} 
          />
          
          <div className={styles.logoWrapper}>
            <h1 className={styles.title}>
              Visnyk<span className={styles.accent}>.</span>
            </h1>
            <p className={styles.slogan}>
              Оперативні новини України
            </p>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;