import React, { useState, useEffect } from 'react';
import axios from 'axios';
import styles from './NewsFeed.module.css';

const NewsFeed = () => {
  const [news, setNews] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // 1. Створюємо контролер для скасування запиту
    const controller = new AbortController();

    const fetchNews = async () => {
      try {
        setLoading(true);
        // 2. Передаємо сигнал контролера в axios
        const response = await axios.get('http://localhost:8000/api/v1/news/', {
          signal: controller.signal
        });
        setNews(response.data);
        setError(null);
      } catch (err) {
        // 3. Якщо помилка викликана скасуванням запиту — ігноруємо її
        if (axios.isCancel(err)) {
          console.log('Запит скасовано:', err.message);
          return;
        }
        console.error("Помилка при завантаженні новин:", err);
        setError('Не вдалося завантажити стрічку новин. Спробуйте пізніше.');
      } finally {
        // Оновлюємо стан завантаження, тільки якщо компонент ще активний
        if (!controller.signal.aborted) {
            setLoading(false);
        }
      }
    };

    fetchNews();

    // 4. Функція очистки: спрацьовує, коли компонент зникає або перезапускається useEffect
    return () => {
      controller.abort();
    };
  }, []);

  const formatDate = (dateString) => {
    const options = { 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric', 
      hour: '2-digit', 
      minute: '2-digit' 
    };
    return new Date(dateString).toLocaleDateString('uk-UA', options);
  };

  const getSourceName = (id) => {
    const sources = {
      1: 'Bloomberg',
      2: 'Reuters',
      3: 'The Economist',
      4: 'Forbes'
    };
    return sources[id] || 'Source #' + id; 
  };

  if (loading) return <div className={styles.loading}>Завантаження новин...</div>;
  if (error) return <div className={styles.error}>{error}</div>;

  return (
    <div className={styles.feedContainer}>
      {news.map((item, index) => (
        <article key={index} className={styles.newsItem}>
          <h2 className={styles.title}>{item.title}</h2>
          <p className={styles.summary}>{item.summary}</p>
          <footer className={styles.metaFooter}>
            <div className={styles.metaInfo}>
              <span className={styles.source}>
                {getSourceName(item.news_source_id)}
              </span>
              <span>•</span>
              <time dateTime={item.published}>
                {formatDate(item.published)}
              </time>
            </div>
            <a 
              href={item.link} 
              target="_blank" 
              rel="noopener noreferrer" 
              className={styles.readMore}
            >
              Читати статтю
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M5 12h14"></path>
                <path d="m12 5 7 7-7 7"></path>
              </svg>
            </a>
          </footer>
        </article>
      ))}
    </div>
  );
};

export default NewsFeed;