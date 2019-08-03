<template>
    <div class="warpper flex">
        <div class="sidebar position-ab">
            <h3>Function</h3>
            <Tree></Tree>
        </div>
        <div class="content">
            <div class="flex">
                <el-button type="primary" @click="btn" size="mini">btn <i :class="{'el-icon-d-arrow-left': isActive,'el-icon-d-arrow-right ' : !isActive}"></i></el-button>
            </div>
        </div>
    </div>
</template>
<script>
import { login } from '@/api/serverApi'
import Tree from './FunctionTree'
import { setTimeout } from 'timers';
export default {
    components: {
        Tree
    },
    data () {
        return {
           className: 'el-icon-d-arrow-left',
           isActive: true
        }
    },
    mounted () {
       
    },
    methods: {
       btn () {
           let getClassSidebar = document.getElementsByClassName('sidebar')
        //    let getSidebarWidth = getClassSidebar[0].offsetWidth
           getClassSidebar[0].classList.toggle('collapsed')
           setTimeout(() => {
               this.isActive = !this.isActive
           }, 100)
       }
    }
}
</script>
<style lang="scss">
@import '@/style/commonStyle.scss';

</style>
