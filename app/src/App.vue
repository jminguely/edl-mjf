<template>
  <div id="app">
    <header class="app-header">
      <div class="container">
        <h1 class="app-title">MJF EDL Stats</h1>
        <nav class="nav-tabs">
          <router-link to="/" class="nav-tab">
            <span class="nav-icon">📊</span>
            Concert Details
          </router-link>
          <router-link to="/summary" class="nav-tab">
            <span class="nav-icon">📈</span>
            All Concerts
          </router-link>
        </nav>
      </div>
    </header>
    <main class="main-content">
      <div class="container">
        <router-view />
      </div>
    </main>
  </div>
</template>

<script>
export default {
  name: "App",
};
</script>

<style>
@import url("https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap");

@font-face {
  font-family: "Vulf";
  src: url("@/assets/fonts/VulfMono-Bold.woff2") format("woff2");
  font-weight: 700;
  font-style: normal;
}

@font-face {
  font-family: "Vulf";
  src: url("@/assets/fonts/VulfMono-Light.woff2") format("woff2");
  font-weight: 300;
  font-style: normal;
}

@font-face {
  font-family: "Vulf";
  src: url("@/assets/fonts/VulfMono-Regular.woff2") format("woff2");
  font-weight: normal;
  font-style: normal;
}

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

html {
  background: linear-gradient(135deg, #0f0f23 0%, #1a1a3e 50%, #000b38 100%);
  color: #e5e7eb;
  min-height: 100vh;
}

body {
  font-family: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui,
    sans-serif;
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1.5rem;
}

.app-header {
  background: rgba(15, 15, 35, 0.95);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  position: sticky;
  top: 0;
  z-index: 100;
  padding: 1rem 0;
}

.app-title {
  font-size: 1.75rem;
  font-weight: 700;
  background: linear-gradient(135deg, #60a5fa, #a78bfa, #f472b6);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 1rem;
  text-align: center;
}

.nav-tabs {
  display: flex;
  gap: 0.5rem;
  justify-content: center;
}

.nav-tab {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  text-decoration: none;
  color: #9ca3af;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 0.75rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
  font-weight: 500;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  backdrop-filter: blur(10px);
}

.nav-tab:hover {
  color: #e5e7eb;
  background: rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 255, 255, 0.2);
  transform: translateY(-1px);
}

.nav-tab.router-link-active {
  color: #fff;
  background: linear-gradient(135deg, #3b82f6, #8b5cf6);
  border-color: transparent;
  box-shadow: 0 10px 25px -5px rgba(59, 130, 246, 0.3);
}

.nav-icon {
  font-size: 1.1rem;
}

.main-content {
  flex: 1;
  padding: 2rem 0;
}

@media (max-width: 768px) {
  .container {
    padding: 0 1rem;
  }

  .app-title {
    font-size: 1.5rem;
  }

  .nav-tabs {
    flex-direction: column;
    gap: 0.75rem;
  }

  .nav-tab {
    justify-content: center;
    padding: 1rem;
  }
}
</style>
