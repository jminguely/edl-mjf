<template>
  <div class="loading-container">
    <div class="spinner">
      <div class="spinner-ring"></div>
      <div class="spinner-ring"></div>
      <div class="spinner-ring"></div>
    </div>
    <p class="loading-text">{{ text || "Loading..." }}</p>
  </div>
</template>

<script>
export default {
  name: "LoadingSpinner",
  props: {
    text: {
      type: String,
      default: "Loading...",
    },
  },
};
</script>

<style scoped>
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  padding: 2rem;
}

.spinner {
  position: relative;
  width: 60px;
  height: 60px;
}

.spinner-ring {
  position: absolute;
  border: 3px solid transparent;
  border-top: 3px solid #60a5fa;
  border-radius: 50%;
  animation: spin 1.2s linear infinite;
}

.spinner-ring:nth-child(1) {
  width: 60px;
  height: 60px;
  animation-delay: 0s;
}

.spinner-ring:nth-child(2) {
  width: 45px;
  height: 45px;
  top: 7.5px;
  left: 7.5px;
  border-top-color: #a78bfa;
  animation-delay: -0.4s;
}

.spinner-ring:nth-child(3) {
  width: 30px;
  height: 30px;
  top: 15px;
  left: 15px;
  border-top-color: #f472b6;
  animation-delay: -0.8s;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.loading-text {
  color: #9ca3af;
  font-weight: 500;
  font-size: 1rem;
  margin: 0;
}
</style>
