import React, { useState, useEffect, useRef } from 'react';
import styles from './FiltersBar.module.css';

const FiltersBar = ({onDateChange, currentDate}) => {
  const [selectedCategory, setSelectedCategory] = useState('Усі новини');

  const [isCategoryOpen, setIsCategoryOpen] = useState(false);

  const categoryRef = useRef(null);

  const categories = [
    'Усі новини', 'Політика', 'Війна', 'Економіка', 'Технології', 'Медицина', 'Спорт'
  ];


  // Закриття меню при кліку поза ним
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (categoryRef.current && !categoryRef.current.contains(event.target)) {
        setIsCategoryOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  return (
    <div className={styles.bar}>
      <div className={styles.container}>

        {/* --- Dropdown: Категорії --- */}
        <div className={styles.dropdownWrapper} ref={categoryRef}>
          <button 
            className={styles.dropdownButton} 
            onClick={() => setIsCategoryOpen(!isCategoryOpen)}
          >
            <div className={styles.buttonContent}>
              <span>{selectedCategory}</span>
            </div>
            {/* Стрілочка вниз */}
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{ transform: isCategoryOpen ? 'rotate(180deg)' : 'rotate(0deg)', transition: 'transform 0.2s' }}>
              <polyline points="6 9 12 15 18 9"></polyline>
            </svg>
          </button>

          {isCategoryOpen && (
            <div className={styles.menu}>
              {categories.map((cat) => (
                <button
                  key={cat}
                  className={`${styles.menuItem} ${selectedCategory === cat ? styles.active : ''}`}
                  onClick={() => {
                    setSelectedCategory(cat);
                    setIsCategoryOpen(false);
                    console.log(`Вибрано категорію: ${cat}`); // Тут буде логіка сортування
                  }}
                >
                  {cat}
                </button>
              ))}
            </div>
          )}
        </div>

        {/* --- Dropdown: Час --- */}
        <div className={styles.datePickerWrapper}>
          <input 
            type="date" 
            className={styles.dateInput}
            value={currentDate}
            onChange={(e) => onDateChange(e.target.value)}
          />
          {/* Кастомна іконка календаря (опціонально) */}
          <span className={styles.calendarIcon}>📅</span>
        </div>

      </div>
    </div>
  );
};

export default FiltersBar;