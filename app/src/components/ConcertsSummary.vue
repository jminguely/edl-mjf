<template>
  <div>
    <h1>MJF EDL STATS: All Concerts</h1>
    <table>
      <tr class="sum">
        <th @click="sortBy('filename')">CONCERT</th>
        <th @click="sortBy('clip_master_duration')">DURATION</th>
        <th @click="sortBy('total_cuts')">CUTS</th>
        <th @click="sortBy('cuts_per_minute')">CUT/MIN.</th>
        <th @click="sortBy('top_longest_cut_duration')">LONGEST CUT</th>
      </tr>
      <tr v-if="loading" class="loading-bar">
        <td>Loading...</td>
      </tr>
      <tr v-for="concert in sortedData" :key="concert.filename">
        <th>{{ concert.filename }}</th>
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

    const sortedData = computed(() => {
      return data.value.slice().sort((a, b) => {
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
