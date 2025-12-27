import Header from './components/Header';
import FiltersBar from './components/FiltersBar';
import NewsFeed from './components/NewsFeed';

const App = () => {
  return (
    <div style={{ minHeight: '100vh', backgroundColor: '#f9fafb' }}>
      
      {/* Верхня частина: Хедер + Фільтри */}
      <nav>
        <Header />
        <FiltersBar />
      </nav>

      {/* Основний контент */}
      <main>
        {/* Заголовок секції (опціонально) */}
        <div style={{ width: '70%', margin: '2rem auto 0 auto' }}>
             <h3 style={{ fontSize: '1.5rem', fontWeight: 'bold' }}>Останні новини</h3>
        </div>

        {/* Компонент стрічки новин */}
        <NewsFeed />
      </main>

    </div>
  );
};

export default App;