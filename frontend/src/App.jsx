import { useState } from 'react';
import Header from './components/Header';
import NavBar from './components/NavBar';
import FiltersBar from './components/FiltersBar';
import NewsFeed from './components/NewsFeed';
import Agent from './components/Agent';

const App = () => {
  const [activeTab, setActiveTab] = useState('fresh');
  const [selectedDate, setSelectedDate] = useState(new Date().toLocaleDateString('en-CA'));
  const [selectedCategory, setSelectedCategory] = useState('Усі новини');

  return (
    <div style={{ minHeight: '100vh', backgroundColor: '#f9fafb' }}>
      
      <nav>
        <Header />
        <NavBar activeTab={activeTab} setActiveTab={setActiveTab}/>
      </nav>

      <main>
        {activeTab === 'agent' ? (
          <Agent />
        ) : (
          <>
          <FiltersBar 
            onDateChange={setSelectedDate} 
            currentDate={selectedDate} 
            activeTab={activeTab} 
            selectedCategory={selectedCategory}
            setSelectedCategory={setSelectedCategory}
          />
          <div style={{ width: '70%', margin: '2rem auto 0 auto' }}>
            <h3 style={{ fontSize: '1.5rem', fontWeight: 'bold' }}>
              {activeTab === 'fresh' ? 'Свіжі новини' : 'Важливі новини'}
            </h3>
          </div>

          <NewsFeed tab={activeTab} date={selectedDate} category={selectedCategory}/>
        </>
        )}
      </main>

    </div>
  );
};

export default App;