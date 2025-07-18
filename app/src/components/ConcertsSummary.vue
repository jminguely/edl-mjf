<template>
  <div>
    <h1>MJF EDL STATS: All Concerts</h1>
    <div style="margin-bottom: 1rem">
      <label for="yearFilter">Filter by year: </label>
      <select id="yearFilter" v-model="selectedYear" @change="filterByYear">
        <option value="">All Years</option>
        <option v-for="year in availableYears" :key="year" :value="year">
          {{ year }}
        </option>
      </select>
    </div>
    <table>
      <tr class="sum">
        <th @click="sortBy('filename')">CONCERT</th>
        <th @click="sortBy('year')">YEAR</th>
        <th @click="sortBy('clip_master_duration')">DURATION</th>
        <th @click="sortBy('total_cuts')">CUTS</th>
        <th @click="sortBy('cuts_per_minute')">CUT/MIN.</th>
        <th @click="sortBy('top_longest_cut_duration')">LONGEST CUT</th>
      </tr>
      <tr v-if="loading" class="loading-bar">
        <td colspan="6">Loading...</td>
      </tr>
      <tr v-for="concert in sortedData" :key="concert.filename">
        <th>{{ concert.filename }}</th>
        <td>{{ concert.year }}</td>
        <td>{{ concert.clip_master_duration }}</td>
        <td>{{ concert.total_cuts }}</td>
        <td>{{ concert.cuts_per_minute }}</td>
        <td>
          {{ concert.top_longest_cut_duration }} (CAM{{
            concert.top_longest_cut_cam
          }})
        </td>
      </tr>
    </table>
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
    const selectedYear = ref("");

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

    return {
      data,
      sortKey,
      sortOrder,
      sortBy,
      sortedData,
      loading,
      selectedYear,
      availableYears,
      filterByYear,
    };
  },
};
</script>

<style lang="postcss" scoped>
h2 {
  margin: 15px 0 0;
  font-weight: 300;
}
table {
  border-collapse: collapse;
  width: 100%;

  td,
  th {
    padding: 5px 10px;
  }

  th {
    text-align: left;
    cursor: pointer;
  }

  tr {
    border-bottom: 1px solid #666;

    &:nth-child(odd):not(.sum) {
      background: #ffffff11;
    }
  }

  tr.sum {
    background: #eee;
    color: #000b68;
  }
}
</style>
