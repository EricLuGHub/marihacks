import Rankings from './components/Rankings.js';
import Navbar from './components/Navbar.js';
import Ticker from './components/Ticker.js';
import Trades from './components/Trades.js';

import './App.css';

function App() {
  return (
    <div className="App">
      <Navbar></Navbar>
      <div id="main">
        <Rankings></Rankings>
        <Trades></Trades>
      </div>
      <Ticker></Ticker>
    </div>
  );
}

export default App;
