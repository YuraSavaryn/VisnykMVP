import React, { useState, useEffect } from 'react';
import axios from 'axios';
import styles from './NewsFeed.module.css';

const NewsFeed = ({tab, date, category}) => {
  const [news, setNews] = useState([]);
  const [sources, setSources] = useState({}); 
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const categoryMapping = {
    'Усі новини': 'unknown',
    'Політика': 'politics',
    'Війна': 'war',
    'Економіка': 'economics',
    'Технології': 'technology',
    'Медицина': 'medicine',
    'Культура': 'culture',
    'Наука': 'science',
    'Освіта': 'education',
    'Шоу-бізнес': 'show business',
    'Спорт': 'sport'
  };

  useEffect(() => {
    const controller = new AbortController();

    const batch_size = 20;
    const categorySystemName = categoryMapping[category] || 'unknown';
    const url = tab === 'fresh' 
      ? `/${date}/${categorySystemName}/${batch_size}` 
      : `/worthy_news/${date}/${batch_size}/`;

    const fetchData = async () => {
      try {
        setLoading(true);
        
        const newsResponse = await axios.get(`http://localhost:8000/api/v1/news${url}`, {
          signal: controller.signal
        });
        
        const newsData = newsResponse.data;
        
        const uniqueSourceIds = [...new Set(newsData.map(item => item.news_source_id))];

        let sourcesMap = {};
        
        if (uniqueSourceIds.length > 0) {
          const sourcesResponse = await axios.get('http://localhost:8000/api/v1/news_source/', {
            params: {
              ids: uniqueSourceIds
            },
            paramsSerializer: {
                indexes: null 
            },
            signal: controller.signal
          });

          sourcesResponse.data.forEach(source => {
            sourcesMap[source.id] = source;
          });
        }

        setNews(newsData);
        setSources(sourcesMap);
        setError(null);

      } catch (err) {
        if (axios.isCancel(err)) {
          console.log('Запит скасовано:', err.message);
          return;
        }
        console.error("Помилка при завантаженні даних:", err);
        setError('Не вдалося завантажити стрічку новин. Спробуйте пізніше.');
      } finally {
        if (!controller.signal.aborted) {
            setLoading(false);
        }
      }
    };

    fetchData();

    return () => {
      controller.abort();
    };
  }, [tab, date, category]);

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

  if (loading) return <div className={styles.loading}>Завантаження новин...</div>;
  if (error) return <div className={styles.error}>{error}</div>;

  return (
    <div className={styles.feedContainer}>
      {news.map((item, index) => {
        // Отримуємо джерело з нашого стейту-мапи
        const sourceData = sources[item.news_source_id];
        
        return (
          <article key={index} className={styles.newsItem}>
            <h2 className={styles.title}>{item.title}</h2>
            <p className={styles.summary}>{item.summary}</p>
            <footer className={styles.metaFooter}>
              <div className={styles.metaInfo}>
                {/* Відображаємо назву джерела або ID, якщо назва ще не завантажилась */}
                <span className={styles.source}>
                  {sourceData ? sourceData.source_title : `Джерело #${item.news_source_id}`}
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
        );
      })}
    </div>
  );
};

export default NewsFeed;