import React, { useState, useEffect, useRef } from 'react';
import styles from './FiltersBar.module.css';

const FiltersBar = () => {
  // Стан для відслідковування активних фільтрів
  const [selectedCategory, setSelectedCategory] = useState('Усі новини');
  const [selectedTime, setSelectedTime] = useState('За сьогодні');

  // Стан для видимості меню (відкрито/закрито)
  const [isCategoryOpen, setIsCategoryOpen] = useState(false);
  const [isTimeOpen, setIsTimeOpen] = useState(false);

  // Рефи для обробки кліків поза елементом (щоб закрити меню, коли клікаєш деінде)
  const categoryRef = useRef(null);
  const timeRef = useRef(null);

  // Список опцій
  const categories = [
    'Усі новини', 'Політика', 'Війна', 'Економіка', 'Технології', 'Медицина', 'Спорт'
  ];

  const timeOptions = [
    'За сьогодні', 'За минулі дні', 'За минулий тиждень'
  ];

  // Закриття меню при кліку поза ним
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (categoryRef.current && !categoryRef.current.contains(event.target)) {
        setIsCategoryOpen(false);
      }
      if (timeRef.current && !timeRef.current.contains(event.target)) {
        setIsTimeOpen(false);
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
        <div className={styles.dropdownWrapper} ref={timeRef}>
          <button 
            className={styles.dropdownButton} 
            onClick={() => setIsTimeOpen(!isTimeOpen)}
          >
            <div className={styles.buttonContent}>
              <span>{selectedTime}</span>
            </div>
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{ transform: isTimeOpen ? 'rotate(180deg)' : 'rotate(0deg)', transition: 'transform 0.2s' }}>
              <polyline points="6 9 12 15 18 9"></polyline>
            </svg>
          </button>

          {isTimeOpen && (
            <div className={styles.menu}>
              {timeOptions.map((time) => (
                <button
                  key={time}
                  className={`${styles.menuItem} ${selectedTime === time ? styles.active : ''}`}
                  onClick={() => {
                    setSelectedTime(time);
                    setIsTimeOpen(false);
                    console.log(`Вибрано час: ${time}`);
                  }}
                >
                  {time}
                </button>
              ))}
            </div>
          )}
        </div>

      </div>
    </div>
  );
};

export default FiltersBar;