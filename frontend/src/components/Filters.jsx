function Filters({ locations, metrics, filters, onFilterChange, onApplyFilters }) {
  const handleFilterChange = (key, value) => {
    onFilterChange({ ...filters, [key]: value });
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <h2 className="text-xl font-semibold text-eco-primary mb-4">Filter Climate Data</h2>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-4">
        {/* Location Filter */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Location</label>
          <select
            value={filters.locationId}
            onChange={(e) => handleFilterChange('locationId', e.target.value)}
            className="w-full p-2 border border-gray-300 rounded-md focus:ring-eco-primary focus:border-eco-primary"
          >
            <option value="">All Locations</option>
            {locations.map(location => (
              <option key={location.id} value={location.id}>
                {location.name}, {location.country}
              </option>
            ))}
          </select>
        </div>

        {/* Metric Filter */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Metric</label>
          <select
            value={filters.metric}
            onChange={(e) => handleFilterChange('metric', e.target.value)}
            className="w-full p-2 border border-gray-300 rounded-md focus:ring-eco-primary focus:border-eco-primary"
          >
            <option value="">All Metrics</option>
            {metrics.map(metric => (
              <option key={metric.id} value={metric.name}>
                {metric.display_name} ({metric.unit})
              </option>
            ))}
          </select>
        </div>

        {/* Quality Filter */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Min Quality</label>
          <select
            value={filters.qualityThreshold}
            onChange={(e) => handleFilterChange('qualityThreshold', e.target.value)}
            className="w-full p-2 border border-gray-300 rounded-md focus:ring-eco-primary focus:border-eco-primary"
          >
            <option value="">All Quality Levels</option>
            <option value="poor">Poor & Above</option>
            <option value="questionable">Questionable & Above</option>
            <option value="good">Good & Above</option>
            <option value="excellent">Excellent Only</option>
          </select>
        </div>

        {/* Start Date */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Start Date</label>
          <input
            type="date"
            value={filters.startDate}
            onChange={(e) => handleFilterChange('startDate', e.target.value)}
            className="w-full p-2 border border-gray-300 rounded-md focus:ring-eco-primary focus:border-eco-primary"
          />
        </div>

        {/* End Date */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">End Date</label>
          <input
            type="date"
            value={filters.endDate}
            onChange={(e) => handleFilterChange('endDate', e.target.value)}
            className="w-full p-2 border border-gray-300 rounded-md focus:ring-eco-primary focus:border-eco-primary"
          />
        </div>

        {/* Analysis Type */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Analysis Type</label>
          <select
            value={filters.analysisType}
            onChange={(e) => handleFilterChange('analysisType', e.target.value)}
            className="w-full p-2 border border-gray-300 rounded-md focus:ring-eco-primary focus:border-eco-primary"
          >
            <option value="raw">Raw Data</option>
            <option value="summary">Summary Stats</option>
            <option value="trends">Trend Analysis</option>
          </select>
        </div>
      </div>

      <button
        onClick={onApplyFilters}
        className="bg-eco-primary text-white px-6 py-2 rounded-md hover:bg-eco-secondary focus:ring-2 focus:ring-eco-primary focus:ring-offset-2"
      >
        Apply Filters
      </button>
    </div>
  );
}

export default Filters;