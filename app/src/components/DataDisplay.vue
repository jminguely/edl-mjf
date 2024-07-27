<template>
  <div>
    <header>
      <h1>MJF EDL STATS: Detail</h1>
      <label for="concertSelect">Choose a concert: </label>
      <select id="concertSelect" v-model="selectedConcert" @change="fetchData">
        <option v-for="concert in concerts" :key="concert" :value="concert">
          {{ concert }}
        </option>
      </select>
    </header>
    <table>
      <tr class="sum">
        <th colspan="3">general stats</th>
      </tr>
      <tr>
        <td>name</td>
        <td colspan="2">{{ selectedConcert }}</td>
      </tr>
      <tr>
        <td>duration</td>
        <td colspan="2">{{ data.clip_master_duration }}</td>
      </tr>
      <tr>
        <td>total cuts</td>
        <td colspan="2">{{ data.total_cuts }}</td>
      </tr>
      <tr>
        <td>cuts per minutes</td>
        <td colspan="2">{{ data.cuts_per_minute }}</td>
      </tr>

      <tr v-if="data.people && Object.keys(data.people).length > 0">
        <th colspan="3"><h2>operators</h2></th>
      </tr>
      <tr class="sum" v-if="data.people && Object.keys(data.people).length > 0">
        <th>CAM</th>
        <th colspan="2">NAME</th>
      </tr>
      <tr v-for="(person, id) in data.people" :key="id">
        <td>
          <strong>{{ id }}</strong>
        </td>
        <td colspan="2">
          {{ person }}
        </td>
      </tr>
      <tr>
        <th colspan="3"><h2>5 longest cuts</h2></th>
      </tr>
      <tr class="sum">
        <th>CAM</th>
        <th>CUT N°</th>
        <th>DURATION</th>
      </tr>

      <tr v-for="cut in data.top_longest_cuts" :key="cut">
        <td>
          <strong>cam{{ cut.cam }}</strong>
          <span v-if="data.people[`cam${cut.cam}`]">
            ({{ data.people[`cam${cut.cam}`] }})
          </span>
        </td>
        <td>{{ cut.cut }}</td>
        <td>{{ cut.duration }}</td>
      </tr>
      <tr>
        <th colspan="3"><h2>total duration in the PGM by cam</h2></th>
      </tr>
      <tr class="sum">
        <th colspan="2">CAM</th>
        <th>DURATION</th>
      </tr>
      <tr v-for="cam in data.total_durations" :key="cam">
        <td colspan="2">
          <strong>cam{{ cam.cam }}</strong>
          <span v-if="data.people[`cam${cam.cam}`]">
            ({{ data.people[`cam${cam.cam}`] }})
          </span>
        </td>
        <td>{{ cam.total_duration }}</td>
      </tr>
    </table>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import axios from "axios";
import concerts from "@/data/concerts.json"; // Adjust the path to your JSON concert

export default {
  setup() {
    const data = ref({});
    const selectedConcert = ref(concerts[0]);
    const concertsList = ref(concerts);

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

    onMounted(() => {
      fetchData();
    });

    return {
      data,
      selectedConcert,
      concerts: concertsList,
      fetchData,
    };
  },
};
</script>

<style lang="postcss" scoped>
h2 {
  margin: 15px 0 0;
  font-weight: 300;
}
select {
  margin-bottom: 2em;
  font-family: "Vulf Mono", courier;
  font-size: 20px;
}
table {
  border-collapse: collapse;
  width: 100%;

  td,
  th {
    padding: 5px 10px;
  }

  th {
    width: 33.33%;
    text-align: left;
  }

  tr {
    border-bottom: 1px solid #666;

    &:nth-child(odd):not(.sum) {
      background: #ffffff11;
    }
  }

  tr.sum {
    background: #eee;
    color: #000b38;
  }
}
</style>
