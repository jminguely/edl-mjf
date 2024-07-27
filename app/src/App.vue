<template>
  <div id="app">
    <nav>
      <router-link to="/">Concerts</router-link>
      <router-link to="/summary">Summary</router-link>
    </nav>
    <router-view />
  </div>
</template>

<script>
export default {
  name: "App",
};
</script>

<style>
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

html {
  background: #000b38;
  color: #eee;
}

body {
  font-family: "Vulf", courier;
}

nav {
  margin-bottom: 1rem;
}

nav a {
  margin-right: 1rem;
  color: #eee;
  text-decoration: underline;
}

nav a.router-link-active {
  font-weight: bold;
}
</style>
