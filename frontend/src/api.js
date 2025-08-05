/**
 * API service module for making requests to the backend
 */

const API_BASE_URL = "http://localhost:5000/api/v1";

/**
 * Fetch climate data with optional filters
 * @param {Object} filters - Filter parameters
 * @returns {Promise} - API response
 */
export const getClimateData = async (filters = {}) => {
  try {
    const params = new URLSearchParams();

    if (filters.locationId) params.append("location_id", filters.locationId);
    if (filters.startDate) params.append("start_date", filters.startDate);
    if (filters.endDate) params.append("end_date", filters.endDate);
    if (filters.metric) params.append("metric", filters.metric);
    if (filters.qualityThreshold)
      params.append("quality_threshold", filters.qualityThreshold);
    if (filters.perPage) params.append("per_page", filters.perPage);

    const response = await fetch(`${API_BASE_URL}/climate?${params}`);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);

    return await response.json();
  } catch (error) {
    console.error("API Error:", error);
    throw error;
  }
};

/**
 * Fetch all available locations
 * @returns {Promise} - API response
 */
export const getLocations = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/locations`);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);

    return await response.json();
  } catch (error) {
    console.error("API Error:", error);
    throw error;
  }
};

/**
 * Fetch all available metrics
 * @returns {Promise} - API response
 */
export const getMetrics = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/metrics`);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);

    return await response.json();
  } catch (error) {
    console.error("API Error:", error);
    throw error;
  }
};

/**
 * Fetch climate summary statistics with optional filters
 * @param {Object} filters - Filter parameters
 * @returns {Promise} - API response
 */
export const getClimateSummary = async (filters = {}) => {
  try {
    const params = new URLSearchParams();

    if (filters.locationId) params.append("location_id", filters.locationId);
    if (filters.startDate) params.append("start_date", filters.startDate);
    if (filters.endDate) params.append("end_date", filters.endDate);
    if (filters.metric) params.append("metric", filters.metric);
    if (filters.qualityThreshold)
      params.append("quality_threshold", filters.qualityThreshold);

    const response = await fetch(`${API_BASE_URL}/summary?${params}`);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);

    return await response.json();
  } catch (error) {
    console.error("API Error:", error);
    throw error;
  }
};

/**
 * Fetch trend analysis with optional filters
 * @param {Object} filters - Filter parameters
 * @returns {Promise} - API response
 */
export const getTrends = async (filters = {}) => {
  try {
    const params = new URLSearchParams();

    if (filters.locationId) params.append("location_id", filters.locationId);
    if (filters.startDate) params.append("start_date", filters.startDate);
    if (filters.endDate) params.append("end_date", filters.endDate);
    if (filters.metric) params.append("metric", filters.metric);
    if (filters.qualityThreshold)
      params.append("quality_threshold", filters.qualityThreshold);

    const response = await fetch(`${API_BASE_URL}/trends?${params}`);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);

    return await response.json();
  } catch (error) {
    console.error("API Error:", error);
    throw error;
  }
};
