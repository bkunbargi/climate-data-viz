import { useState, useEffect } from 'react';
import Filters from './components/Filters';
import ChartContainer from './components/ChartContainer';
import TrendAnalysis from './components/TrendAnalysis';
import QualityIndicator from './components/QualityIndicator';
import { getLocations, getMetrics, getClimateData, getClimateSummary, getTrends } from './api';

function App() {
  const [locations, setLocations] = useState([]);
  const [metrics, setMetrics] = useState([]);
  const [climateData, setClimateData] = useState([]);
  const [trendData, setTrendData] = useState(null);
  const [filters, setFilters] = useState({
    locationId: '',
    startDate: '',
    endDate: '',
    metric: '',
    qualityThreshold: '',
    analysisType: 'raw'
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Load initial data on component mount
  useEffect(() => {
    const loadInitialData = async () => {
      try {
        const [locationsRes, metricsRes] = await Promise.all([
          getLocations(),
          getMetrics()
        ]);
        
        setLocations(locationsRes.data || []);
        setMetrics(metricsRes.data || []);
        
        const initialData = await getClimateData({ perPage: 50 });
        setClimateData(initialData.data || []);
      } catch (err) {
        console.error('Failed to load initial data:', err);
        setError('Failed to load data. Make sure the backend server is running.');
      }
    };

    loadInitialData();
  }, []);

  // Fetch data based on current filters
  const fetchData = async () => {
    setLoading(true);
    setError(null);
    
    try {
      let data;
      
      if (filters.analysisType === 'trends') {
        data = await getTrends(filters);
        setTrendData(data.data);
        setClimateData([]);
      } else if (filters.analysisType === 'summary') {
        data = await getClimateSummary(filters);
        setClimateData(data.data);
        setTrendData(null);
      } else {
        data = await getClimateData({ ...filters, perPage: 50 });
        setClimateData(data.data || []);
        setTrendData(null);
      }
    } catch (err) {
      console.error('Error fetching data:', err);
      setError('Failed to fetch data. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mx-auto px-4 py-8 max-w-6xl">
      <header className="mb-8 text-center">
        <h1 className="text-4xl font-bold text-eco-primary mb-2">
          EcoVision: Climate Visualizer
        </h1>
        <p className="text-gray-600 italic">
          Transforming climate data into actionable insights for a sustainable future
        </p>
      </header>

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}

      <Filters 
        locations={locations}
        metrics={metrics}
        filters={filters}
        onFilterChange={setFilters}
        onApplyFilters={fetchData}
      />

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-8">
        {filters.analysisType === 'trends' ? (
          <div className="lg:col-span-2">
            <TrendAnalysis 
              data={trendData}
              loading={loading}
            />
          </div>
        ) : (
          <>
            <ChartContainer 
              title="Climate Data"
              loading={loading}
              chartType="line"
              data={climateData}
              showQuality={true}
            />
            <ChartContainer 
              title="Data Overview"
              loading={loading}
              chartType="bar"
              data={climateData}
              showQuality={true}
            />
          </>
        )}
      </div>

      <QualityIndicator 
        data={climateData}
        className="mt-6"
      />
    </div>
  );
}

export default App;