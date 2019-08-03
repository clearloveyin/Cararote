<template>
    <div id="app">
        <!-- <div class="header"> -->
            <!-- <router-link to="/">Home</router-link> -->
            <!-- <router-link to="/about">About</router-link> -->
            <!-- <Nav></Nav> -->
        <!-- </div> -->
        <router-view/>
    </div>
</template>
<script>
// import Nav from '@/views/headerPage/Nav.vue'
export default {
  name: 'App'
}
</script>
<style lang="scss">
    @import './style/App.scss';
</style>
