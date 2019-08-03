<template>
    <div class="home">
        <div class="header">
            <Nav></Nav>
        </div>
        <router-view/>
    </div>
</template>
<script>
import Nav from '@/views/headerPage/Nav.vue'
export default {
  name: 'Home',
  components: { Nav }
}
</script>
<style lang="scss" scoped>
</style>
