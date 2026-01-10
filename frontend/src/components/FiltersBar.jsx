import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import styles from './FiltersBar.module.css';

const FiltersBar = ({ onDateChange, currentDate, activeTab, selectedCategory, setSelectedCategory }) => {
  const [isCategoryOpen, setIsCategoryOpen] = useState(false);
  const [isEvaluating, setIsEvaluating] = useState(false);

  const categoryRef = useRef(null);
  const categories = ['Усі новини', 'Політика', 'Війна', 'Економіка', 'Технології', 'Медицина', 
    'Культура', 'Наука', 'Освіта', 'Шоу-бізнес', 'Спорт'];

  const handleEvaluate = async () => {
    try {
      setIsEvaluating(true);
      await axios.post(`http://localhost:8000/api/v1/model/evaluate_news_ner`, null, {
        params: { certain_date: currentDate }
      });
      alert('Аналіз новий запущено!');
    } catch (error) {
      console.error("Помилка:", error);
      alert('Помилка при запуску аналізу.');
    } finally {
      setIsEvaluating(false);
    }
  };

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
        
        <div className={styles.leftGroup}>
          <div className={styles.dropdownWrapper} ref={categoryRef}>
            <button 
              className={styles.dropdownButton} 
              onClick={() => setIsCategoryOpen(!isCategoryOpen)}
            >
              <span>{selectedCategory}</span>
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" style={{ transform: isCategoryOpen ? 'rotate(180deg)' : 'rotate(0deg)', transition: 'transform 0.2s' }}>
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
                    }}
                  >
                    {cat}
                  </button>
                ))}
              </div>
            )}
          </div>

          <div className={styles.datePickerWrapper}>
            <input 
              type="date" 
              className={styles.dateInput}
              value={currentDate}
              onChange={(e) => onDateChange(e.target.value)}
            />
          </div>
        </div>

        {activeTab === 'important' && (
          <button 
            className={styles.evaluateButton} 
            onClick={handleEvaluate}
            disabled={isEvaluating}
          >
            {isEvaluating ? 'Обробка...' : 'Аналізувати новини'}
          </button>
        )}

      </div>
    </div>
  );
};

export default FiltersBar;