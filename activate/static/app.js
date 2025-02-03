// Use React hooks available via the React global object.
const { useState, useEffect } = React;

function App() {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  const fetchData = () => {
    fetch('/api/gpu_data')
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        setData(data);
        setError(null);
      })
      .catch(err => {
        setError(err.toString());
      });
  };

  // Fetch data immediately, and then every 5 seconds.
  useEffect(() => {
    fetchData();
    const intervalId = setInterval(fetchData, 5000);
    return () => clearInterval(intervalId);
  }, []);

  return (
    <div>
      <h1>GPU Topology Monitor</h1>
      {error && <div style={{ color: 'red' }}>Error: {error}</div>}
      {data ? <pre>{JSON.stringify(data, null, 2)}</pre> : <p>Loading data...</p>}
    </div>
  );
}

ReactDOM.render(<App />, document.getElementById('root'));
