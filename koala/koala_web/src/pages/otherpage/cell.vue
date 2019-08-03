<template>
    <div id="cell">
        <my-component v-if="component_flag"></my-component>
        <my-component-html v-else></my-component-html>
    </div>
</template>

<script>
import handHtml from './inputHtml.vue'
import handTable from './handsontable/handsontable_demo'
export default {
    name: 'cell',
    components: {
        'my-component': handTable,
        'my-component-html': handHtml,
    },
    data() {
        return {
            component_flag:true,
        }
    },
    created() {
        if (location.search == '?input') {
            this.component_flag = false
        }else{
            this.component_flag = true
        }
    },
}
</script>

<style>
#cell {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    height: 100%;
    width: 100%;
}
html,
body {
    margin: 0;
    padding: 0;
    height: 100%;
    width: 100%;
    overflow: hidden;
}
</style>
