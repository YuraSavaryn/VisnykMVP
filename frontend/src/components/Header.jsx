import React from 'react';
import styles from './Header.module.css';

const Header = () => {
  return (
    <header className={styles.header}>
      <div className={styles.container}>
        
        {/* Логотип та слоган */}
        <div className={styles.logoWrapper}>
          <h1 className={styles.title}>
            Visnyk<span className={styles.accent}>.</span>
          </h1>
          <p className={styles.slogan}>
            Оперативні новини України
          </p>
        </div>

        {/* Соціальні іконки */}
        <div className={styles.socials}>
          
          {/* Email Icon */}
          <a href="mailto:info@visnyk.com" className={styles.iconLink} aria-label="Email">
            <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <rect width="20" height="16" x="2" y="4" rx="2" />
              <path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7" />
            </svg>
          </a>

          {/* Instagram Icon */}
          <a href="https://instagram.com" target="_blank" rel="noopener noreferrer" className={styles.iconLink} aria-label="Instagram">
            <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <rect width="20" height="20" x="2" y="2" rx="5" ry="5" />
              <path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z" />
              <line x1="17.5" x2="17.51" y1="6.5" y2="6.5" />
            </svg>
          </a>

          {/* Telegram Icon */}
          <a href="https://t.me" target="_blank" rel="noopener noreferrer" className={styles.iconLink} aria-label="Telegram">
            <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <line x1="22" x2="11" y1="2" y2="13" />
              <polygon points="22 2 15 22 11 13 2 9 22 2" />
            </svg>
          </a>

        </div>
      </div>
    </header>
  );
};

export default Header;