<template>
  <div class="data-display">
    <div class="controls-section">
      <div class="control-group">
        <label for="yearFilter" class="control-label">
          <span class="label-icon">📅</span>
          Filter by year
        </label>
        <select
          id="yearFilter"
          v-model="selectedYear"
          @change="filterConcertsByYear"
          class="modern-select"
        >
          <option value="">All Years</option>
          <option v-for="year in availableYears" :key="year" :value="year">
            {{ year }}
          </option>
        </select>
      </div>

      <div class="control-group">
        <label for="concertSelect" class="control-label">
          <span class="label-icon">🎵</span>
          Choose a concert
        </label>
        <select
          id="concertSelect"
          v-model="selectedConcert"
          @change="fetchData"
          class="modern-select"
        >
          <option
            v-for="concert in filteredConcerts"
            :key="concert"
            :value="concert"
          >
            {{ concert }}
          </option>
        </select>
      </div>
    </div>

    <div v-if="selectedConcert" class="stats-grid">
      <!-- General Stats Card -->
      <div class="stats-card featured">
        <div class="card-header">
          <h2 class="card-title">
            <span class="title-icon">📊</span>
            General Statistics
          </h2>
        </div>
        <div class="card-content">
          <div class="stat-row">
            <span class="stat-label">Concert</span>
            <span class="stat-value">{{ selectedConcert }}</span>
          </div>
          <div class="stat-row">
            <span class="stat-label">Duration</span>
            <span class="stat-value">{{ data.clip_master_duration }}</span>
          </div>
          <div class="stat-row">
            <span class="stat-label">Total Cuts</span>
            <span class="stat-value highlight">{{ data.total_cuts }}</span>
          </div>
          <div class="stat-row">
            <span class="stat-label">Cuts per Minute</span>
            <span class="stat-value highlight">{{ data.cuts_per_minute }}</span>
          </div>
        </div>
      </div>

      <!-- Operators Card -->
      <div
        v-if="data.people && Object.keys(data.people).length > 0"
        class="stats-card"
      >
        <div class="card-header">
          <h2 class="card-title">
            <span class="title-icon">👥</span>
            Camera Operators
          </h2>
        </div>
        <div class="card-content">
          <div class="operators-grid">
            <div
              v-for="(person, id) in data.people"
              :key="id"
              class="operator-item"
            >
              <span class="cam-badge">{{ id.toUpperCase() }}</span>
              <span class="operator-name">{{ person }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Longest Cuts Card -->
      <div class="stats-card">
        <div class="card-header">
          <h2 class="card-title">
            <span class="title-icon">⏱️</span>
            Top 5 Longest Cuts
          </h2>
        </div>
        <div class="card-content">
          <div class="cuts-list">
            <div
              v-for="(cut, index) in data.top_longest_cuts"
              :key="index"
              class="cut-item"
              :class="{ 'top-cut': index === 0 }"
            >
              <div class="cut-rank">#{{ index + 1 }}</div>
              <div class="cut-info">
                <div class="cut-camera">
                  <span class="cam-badge">CAM{{ cut.cam }}</span>
                  <span
                    v-if="data.people[`cam${cut.cam}`]"
                    class="operator-mini"
                  >
                    {{ data.people[`cam${cut.cam}`] }}
                  </span>
                </div>
                <div class="cut-details">
                  <div class="cut-header">
                    <span class="cut-number">Cut {{ cut.cut }}</span>
                    <span class="cut-timecode">{{ cut.start_timecode }}</span>
                  </div>
                  <span class="cut-duration">{{ cut.duration }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Total Durations Card -->
      <div class="stats-card full-width">
        <div class="card-header">
          <h2 class="card-title">
            <span class="title-icon">📺</span>
            Screen Time by Camera
          </h2>
        </div>
        <div class="card-content">
          <div class="duration-grid">
            <div
              v-for="cam in data.total_durations"
              :key="cam.cam"
              class="duration-item"
            >
              <div class="duration-header">
                <span class="cam-badge large">CAM{{ cam.cam }}</span>
                <span v-if="data.people[`cam${cam.cam}`]" class="operator-name">
                  {{ data.people[`cam${cam.cam}`] }}
                </span>
              </div>
              <div class="duration-value">{{ cam.total_duration }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from "vue";
import axios from "axios";

export default {
  setup() {
    const data = ref({});
    const selectedConcert = ref("");
    const concertsList = ref([]);
    const selectedYear = ref("2025");

    const availableYears = computed(() => {
      const years = [
        ...new Set(concertsList.value.map((concert) => concert.split("-")[0])),
      ];
      return years.sort().reverse();
    });

    const filteredConcerts = computed(() => {
      if (!selectedYear.value) {
        return concertsList.value;
      }
      return concertsList.value.filter((concert) =>
        concert.startsWith(selectedYear.value)
      );
    });

    const fetchConcerts = async () => {
      try {
        const response = await axios.get(
          `https://edl-api.mingus.space/concerts`
        );
        concertsList.value = response.data.map((concert) => concert.name);
        if (concertsList.value.length > 0) {
          // If a year is selected, use the first concert from that year
          if (selectedYear.value && filteredConcerts.value.length > 0) {
            selectedConcert.value = filteredConcerts.value[0];
          } else {
            selectedConcert.value = concertsList.value[0];
          }
          fetchData();
        }
      } catch (error) {
        console.error("Error fetching concerts:", error);
        // Fallback to static data if API fails
        const concerts = await import("@/data/concerts.json");
        concertsList.value = concerts.default;
        if (selectedYear.value && filteredConcerts.value.length > 0) {
          selectedConcert.value = filteredConcerts.value[0];
        } else {
          selectedConcert.value = concertsList.value[0];
        }
        fetchData();
      }
    };

    const fetchData = async () => {
      try {
        const response = await axios.get(
          `https://edl-api.mingus.space/edlstats?concert=${selectedConcert.value}`
        );
        data.value = response.data;
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    const filterConcertsByYear = () => {
      if (filteredConcerts.value.length > 0) {
        selectedConcert.value = filteredConcerts.value[0];
        fetchData();
      }
    };

    onMounted(() => {
      fetchConcerts();
    });

    return {
      data,
      selectedConcert,
      concerts: concertsList,
      selectedYear,
      availableYears,
      filteredConcerts,
      filterConcertsByYear,
      fetchData,
    };
  },
};
</script>

<style lang="postcss" scoped>
.data-display {
  max-width: 100%;
}

.controls-section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
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

.modern-select option {
  background: #1e293b;
  color: #e5e7eb;
  padding: 0.5rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 1.5rem;
  align-items: start;
}

.stats-card {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 1rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  overflow: hidden;
  transition: all 0.3s ease;
}

.stats-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.3);
  border-color: rgba(255, 255, 255, 0.2);
}

.stats-card.featured {
  background: linear-gradient(
    135deg,
    rgba(59, 130, 246, 0.1),
    rgba(139, 92, 246, 0.1)
  );
  border-color: rgba(59, 130, 246, 0.3);
}

.stats-card.full-width {
  grid-column: 1 / -1;
}

.card-header {
  padding: 1.5rem 1.5rem 0;
}

.card-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.25rem;
  font-weight: 600;
  color: #f3f4f6;
  margin: 0;
}

.title-icon {
  font-size: 1.5rem;
}

.card-content {
  padding: 1.5rem;
}

.stat-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.stat-row:last-child {
  border-bottom: none;
}

.stat-label {
  font-weight: 500;
  color: #9ca3af;
  text-transform: capitalize;
}

.stat-value {
  font-weight: 600;
  color: #e5e7eb;
  font-family: "Vulf", monospace;
}

.stat-value.highlight {
  color: #60a5fa;
  background: rgba(96, 165, 250, 0.1);
  padding: 0.25rem 0.5rem;
  border-radius: 0.375rem;
}

.operators-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1rem;
}

.operator-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 0.5rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.cam-badge {
  display: inline-block;
  padding: 0.25rem 0.5rem;
  background: linear-gradient(135deg, #3b82f6, #8b5cf6);
  color: white;
  font-weight: 600;
  font-size: 0.75rem;
  border-radius: 0.375rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.cam-badge.large {
  padding: 0.5rem 0.75rem;
  font-size: 0.875rem;
}

.operator-name {
  font-weight: 500;
  color: #e5e7eb;
}

.cuts-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.cut-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 0.75rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
}

.cut-item.top-cut {
  background: linear-gradient(
    135deg,
    rgba(245, 158, 11, 0.1),
    rgba(251, 191, 36, 0.1)
  );
  border-color: rgba(245, 158, 11, 0.3);
}

.cut-item:hover {
  background: rgba(255, 255, 255, 0.1);
  transform: translateX(4px);
}

.cut-rank {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2rem;
  height: 2rem;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 50%;
  font-weight: 600;
  font-size: 0.875rem;
  color: #9ca3af;
}

.cut-item.top-cut .cut-rank {
  background: linear-gradient(135deg, #f59e0b, #fbbf24);
  color: #000;
}

.cut-info {
  flex: 1;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.cut-camera {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.operator-mini {
  font-size: 0.75rem;
  color: #9ca3af;
  font-weight: 400;
}

.cut-details {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 0.25rem;
}

.cut-header {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 0.125rem;
}

.cut-number {
  font-size: 0.875rem;
  color: #9ca3af;
}

.cut-timecode {
  font-size: 0.75rem;
  color: #6b7280;
  font-family: "Vulf", monospace;
}

.cut-duration {
  font-weight: 600;
  color: #e5e7eb;
  font-family: "Vulf", monospace;
}

.duration-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1rem;
}

.duration-item {
  padding: 1.25rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 0.75rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
  text-align: center;
  transition: all 0.3s ease;
}

.duration-item:hover {
  transform: translateY(-2px);
  background: rgba(255, 255, 255, 0.1);
}

.duration-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.duration-value {
  font-size: 1.25rem;
  font-weight: 700;
  color: #60a5fa;
  font-family: "Vulf", monospace;
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }

  .controls-section {
    grid-template-columns: 1fr;
    padding: 1rem;
  }

  .operators-grid {
    grid-template-columns: 1fr;
  }

  .duration-grid {
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  }

  .cut-info {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }

  .cut-details {
    align-items: flex-start;
  }

  .cut-header {
    align-items: flex-start;
  }
}
</style>
