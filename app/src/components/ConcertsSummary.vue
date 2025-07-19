<template>
  <div class="concerts-summary">
    <div class="page-header">
      <div class="header-content">
        <div class="header-text">
          <h1 class="page-title">All Concerts Overview</h1>
          <p class="page-subtitle">
            Comprehensive statistics for all recorded concerts
          </p>
        </div>
        <div class="stats-summary" v-if="!loading && data.length > 0">
          <div class="summary-item">
            <span class="summary-value">{{ filteredData.length }}</span>
            <span class="summary-label">Concerts</span>
          </div>
          <div class="summary-item">
            <span class="summary-value">{{ availableYears.length }}</span>
            <span class="summary-label">Years</span>
          </div>
        </div>
      </div>
    </div>

    <div class="controls-section">
      <div class="control-group">
        <label for="yearFilter" class="control-label">
          <span class="label-icon">📅</span>
          Filter by Year
        </label>
        <select
          id="yearFilter"
          v-model="selectedYear"
          @change="filterByYear"
          class="modern-select"
        >
          <option value="">All Years ({{ data.length }} concerts)</option>
          <option v-for="year in availableYears" :key="year" :value="year">
            {{ year }} ({{ data.filter((c) => c.year === year).length }}
            concerts)
          </option>
        </select>
      </div>
    </div>

    <div class="table-container">
      <div class="table-wrapper">
        <table class="modern-table">
          <thead>
            <tr class="header-row">
              <th
                @click="sortBy('filename')"
                class="sortable-header"
                :class="getSortClass('filename')"
              >
                <span class="header-content">
                  <span class="header-icon">🎵</span>
                  Concert
                  <span class="sort-indicator">{{
                    getSortIndicator("filename")
                  }}</span>
                </span>
              </th>
              <th
                @click="sortBy('year')"
                class="sortable-header"
                :class="getSortClass('year')"
              >
                <span class="header-content">
                  <span class="header-icon">📅</span>
                  Year
                  <span class="sort-indicator">{{
                    getSortIndicator("year")
                  }}</span>
                </span>
              </th>
              <th
                @click="sortBy('clip_master_duration')"
                class="sortable-header"
                :class="getSortClass('clip_master_duration')"
              >
                <span class="header-content">
                  <span class="header-icon">⏱️</span>
                  Duration
                  <span class="sort-indicator">{{
                    getSortIndicator("clip_master_duration")
                  }}</span>
                </span>
              </th>
              <th
                @click="sortBy('total_cuts')"
                class="sortable-header"
                :class="getSortClass('total_cuts')"
              >
                <span class="header-content">
                  <span class="header-icon">✂️</span>
                  Cuts
                  <span class="sort-indicator">{{
                    getSortIndicator("total_cuts")
                  }}</span>
                </span>
              </th>
              <th
                @click="sortBy('cuts_per_minute')"
                class="sortable-header"
                :class="getSortClass('cuts_per_minute')"
              >
                <span class="header-content">
                  <span class="header-icon">⚡</span>
                  Cut/Min
                  <span class="sort-indicator">{{
                    getSortIndicator("cuts_per_minute")
                  }}</span>
                </span>
              </th>
              <th
                @click="sortBy('top_longest_cut_duration')"
                class="sortable-header"
                :class="getSortClass('top_longest_cut_duration')"
              >
                <span class="header-content">
                  <span class="header-icon">🏆</span>
                  Longest Cut
                  <span class="sort-indicator">{{
                    getSortIndicator("top_longest_cut_duration")
                  }}</span>
                </span>
              </th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="loading" class="loading-row">
              <td colspan="6" class="loading-cell">
                <div class="loading-content">
                  <div class="loading-spinner"></div>
                  <span>Loading concerts data...</span>
                </div>
              </td>
            </tr>
            <tr
              v-for="(concert, index) in sortedData"
              :key="concert.filename"
              class="data-row"
              :class="{
                'highlight-row': index < 3 && sortKey === 'cuts_per_minute',
              }"
            >
              <td class="concert-name">
                <div class="concert-info">
                  <span class="concert-title">{{
                    formatConcertName(concert.filename)
                  }}</span>
                  <span class="concert-venue">{{
                    getVenue(concert.filename)
                  }}</span>
                </div>
              </td>
              <td class="year-cell">
                <span class="year-badge">{{ concert.year }}</span>
              </td>
              <td class="duration-cell">
                <span class="duration-value">{{
                  concert.clip_master_duration
                }}</span>
              </td>
              <td class="cuts-cell">
                <span class="cuts-value">{{ concert.total_cuts }}</span>
              </td>
              <td class="rate-cell">
                <span
                  class="rate-value"
                  :class="getRateClass(concert.cuts_per_minute)"
                >
                  {{ concert.cuts_per_minute }}
                </span>
              </td>
              <td class="longest-cut-cell">
                <div class="longest-cut-info">
                  <span class="cut-duration">{{
                    concert.top_longest_cut_duration
                  }}</span>
                  <span class="cut-camera"
                    >CAM{{ concert.top_longest_cut_cam }}</span
                  >
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from "vue";
import axios from "axios";

export default {
  setup() {
    const loading = ref(false);
    const data = ref([]);
    const sortKey = ref("");
    const sortOrder = ref(1);
    const selectedYear = ref("2025");

    const availableYears = computed(() => {
      const years = [...new Set(data.value.map((concert) => concert.year))];
      return years.sort().reverse(); // Show newest years first
    });

    const filteredData = computed(() => {
      if (!selectedYear.value) {
        return data.value;
      }
      return data.value.filter(
        (concert) => concert.year === selectedYear.value
      );
    });

    const fetchData = async () => {
      loading.value = true;
      try {
        const response = await axios.get(
          `https://edl-api.mingus.space/edlsummary`
        );
        data.value = response.data;
      } catch (error) {
        console.error("Error fetching data:", error);
      } finally {
        loading.value = false;
      }
    };

    const sortBy = (key) => {
      if (sortKey.value === key) {
        sortOrder.value = -sortOrder.value;
      } else {
        sortKey.value = key;
        sortOrder.value = 1;
      }
    };

    const filterByYear = () => {
      // This will trigger the computed property to update
    };

    const sortedData = computed(() => {
      return filteredData.value.slice().sort((a, b) => {
        let result = 0;
        if (a[sortKey.value] < b[sortKey.value]) {
          result = -1;
        } else if (a[sortKey.value] > b[sortKey.value]) {
          result = 1;
        }
        return result * sortOrder.value;
      });
    });

    onMounted(() => {
      fetchData();
    });

    const getSortClass = (key) => {
      return {
        "active-sort": sortKey.value === key,
        "sort-desc": sortKey.value === key && sortOrder.value === -1,
      };
    };

    const getSortIndicator = (key) => {
      if (sortKey.value !== key) return "";
      return sortOrder.value === 1 ? "↑" : "↓";
    };

    const formatConcertName = (filename) => {
      // Extract artist name from filename
      const parts = filename.split("_");
      if (parts.length >= 3) {
        const artist = parts.slice(2, -1).join(" ").replace(/-/g, " ");
        return artist;
      }
      return filename;
    };

    const getVenue = (filename) => {
      // Extract venue from filename (LAC or CASINO)
      const parts = filename.split("_");
      if (parts.length >= 2) {
        const venue = parts[1];
        return venue === "LAC"
          ? "Lac Léman"
          : venue === "CASINO"
          ? "Casino"
          : venue;
      }
      return "";
    };

    const getRateClass = (rate) => {
      const numRate = parseFloat(rate);
      if (numRate >= 8) return "rate-very-high";
      if (numRate >= 6) return "rate-high";
      if (numRate >= 4) return "rate-medium";
      return "rate-low";
    };

    return {
      data,
      sortKey,
      sortOrder,
      sortBy,
      sortedData,
      loading,
      selectedYear,
      availableYears,
      filteredData,
      filterByYear,
      getSortClass,
      getSortIndicator,
      formatConcertName,
      getVenue,
      getRateClass,
    };
  },
};
</script>

<style lang="postcss" scoped>
.concerts-summary {
  max-width: 100%;
}

.page-header {
  margin-bottom: 2rem;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 2rem;
  padding: 0.5rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 1rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
}

.header-text {
  flex: 1;
}

.page-title {
  font-size: 2rem;
  font-weight: 700;
  background: linear-gradient(135deg, #60a5fa, #a78bfa);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin: 0 0 0.5rem 0;
}

.page-subtitle {
  color: #9ca3af;
  font-size: 1rem;
  font-weight: 400;
  margin: 0;
}

.stats-summary {
  display: flex;
  gap: 2rem;
}

.summary-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.25rem;
}

.summary-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: #60a5fa;
  font-family: "Vulf", monospace;
}

.summary-label {
  font-size: 0.75rem;
  color: #9ca3af;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  font-weight: 500;
}

.controls-section {
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 1rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
}

.control-group {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  max-width: 400px;
}

.control-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 500;
  color: #e5e7eb;
  font-size: 0.875rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.label-icon {
  font-size: 1rem;
}

.modern-select {
  padding: 0.875rem 1rem;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 0.5rem;
  color: #fff;
  font-size: 1rem;
  font-weight: 500;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
  appearance: none;
  background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3e%3cpath stroke='%239ca3af' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='m6 8 4 4 4-4'/%3e%3c/svg%3e");
  background-position: right 0.5rem center;
  background-repeat: no-repeat;
  background-size: 1.5em 1.5em;
  padding-right: 2.5rem;
}

.modern-select:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2);
  background: rgba(255, 255, 255, 0.15);
}

.table-container {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 1rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  overflow: hidden;
}

.table-wrapper {
  overflow-x: auto;
}

.modern-table {
  width: 100%;
  border-collapse: collapse;
}

.header-row {
  background: rgba(255, 255, 255, 0.1);
  border-bottom: 2px solid rgba(255, 255, 255, 0.2);
}

.sortable-header {
  padding: 1rem 1.5rem;
  text-align: left;
  cursor: pointer;
  transition: all 0.3s ease;
  user-select: none;
  position: relative;
}

.sortable-header:hover {
  background: rgba(255, 255, 255, 0.15);
}

.sortable-header.active-sort {
  background: rgba(59, 130, 246, 0.2);
}

.header-content {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 500;
  color: #d1d5db;
  text-transform: none;
  letter-spacing: 0.02em;
  font-size: 0.875rem;
}

.header-icon {
  font-size: 0.875rem;
  opacity: 0.6;
}

.sort-indicator {
  margin-left: auto;
  font-size: 0.75rem;
  opacity: 0.5;
  font-weight: normal;
}

.sortable-header.active-sort .sort-indicator {
  opacity: 1;
  color: #9ca3af;
}

.data-row {
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
}

.data-row:hover {
  background: rgba(255, 255, 255, 0.08);
  transform: translateX(2px);
}

.data-row.highlight-row {
  background: rgba(245, 158, 11, 0.1);
  border-color: rgba(245, 158, 11, 0.3);
}

.data-row td {
  padding: 1rem 1.5rem;
  vertical-align: middle;
}

.concert-name {
  min-width: 250px;
}

.concert-info {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.concert-title {
  font-weight: 600;
  color: #e5e7eb;
  text-transform: capitalize;
}

.concert-venue {
  font-size: 0.75rem;
  color: #9ca3af;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  font-weight: 500;
}

.year-cell {
  text-align: center;
}

.year-badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  background: rgba(139, 92, 246, 0.2);
  border: 1px solid rgba(139, 92, 246, 0.3);
  color: #a78bfa;
  font-weight: 600;
  border-radius: 0.375rem;
  font-size: 0.875rem;
}

.duration-cell,
.cuts-cell {
  text-align: center;
}

.duration-value,
.cuts-value {
  font-family: "Vulf", monospace;
  font-weight: 600;
  color: #e5e7eb;
}

.rate-cell {
  text-align: center;
}

.rate-value {
  display: inline-block;
  padding: 0.375rem 0.75rem;
  font-family: "Vulf", monospace;
  font-weight: 700;
  border-radius: 0.375rem;
  font-size: 0.875rem;
}

.rate-value.rate-very-high {
  background: rgba(239, 68, 68, 0.2);
  color: #f87171;
  border: 1px solid rgba(239, 68, 68, 0.3);
}

.rate-value.rate-high {
  background: rgba(245, 158, 11, 0.2);
  color: #fbbf24;
  border: 1px solid rgba(245, 158, 11, 0.3);
}

.rate-value.rate-medium {
  background: rgba(34, 197, 94, 0.2);
  color: #4ade80;
  border: 1px solid rgba(34, 197, 94, 0.3);
}

.rate-value.rate-low {
  background: rgba(59, 130, 246, 0.2);
  color: #60a5fa;
  border: 1px solid rgba(59, 130, 246, 0.3);
}

.longest-cut-cell {
  text-align: center;
}

.longest-cut-info {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  align-items: center;
}

.cut-duration {
  font-family: "Vulf", monospace;
  font-weight: 600;
  color: #e5e7eb;
}

.cut-camera {
  font-size: 0.75rem;
  color: #9ca3af;
  background: rgba(255, 255, 255, 0.1);
  padding: 0.125rem 0.375rem;
  border-radius: 0.25rem;
  font-weight: 500;
}

.loading-row {
  background: rgba(255, 255, 255, 0.05);
}

.loading-cell {
  padding: 3rem 1.5rem;
  text-align: center;
}

.loading-content {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  color: #9ca3af;
  font-weight: 500;
}

.loading-spinner {
  width: 1.5rem;
  height: 1.5rem;
  border: 2px solid rgba(255, 255, 255, 0.2);
  border-top: 2px solid #60a5fa;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

@media (max-width: 1024px) {
  .header-content {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .stats-summary {
    gap: 1rem;
  }

  .page-title {
    font-size: 1.5rem;
  }
}

@media (max-width: 768px) {
  .header-content,
  .controls-section {
    padding: 1rem;
  }

  .control-group {
    max-width: 100%;
  }

  .modern-table {
    font-size: 0.875rem;
  }

  .sortable-header,
  .data-row td {
    padding: 0.75rem 1rem;
  }

  .concert-name {
    min-width: 200px;
  }

  .header-content {
    font-size: 0.75rem;
  }
}

@media (max-width: 640px) {
  .stats-summary {
    flex-direction: column;
    gap: 0.5rem;
  }

  .summary-item {
    flex-direction: row;
    gap: 0.5rem;
  }

  .modern-table {
    font-size: 0.75rem;
  }

  .sortable-header,
  .data-row td {
    padding: 0.5rem;
  }
}
</style>
