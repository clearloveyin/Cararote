<template>
    <div class="warpper">
        <!--头部组件-->
        <div class="menu">
            <el-breadcrumb separator-class="el-icon-arrow-right">
                <el-breadcrumb-item v-for="(item,index) in router" :to="item.path" :replace='item.replace' :key="index">{{item.name}}</el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        
    </div>
</template>

<script>
export default {
    data() {
        return {
            router:[
            ]
        }
    },
    beforeUpdate() {
        
    },
    mounted() {
        this.default_mounted()
    },
    methods: {
        default_mounted(){
            console.log(this.$route)
            let routers = this.$route
            if (routers) {
                for (let item of routers.matched) {
                    if (item.name !== '') {
                        this.router.push(
                            {path:item.path,replace:true,name:item.name}
                        )
                    }
                }
            }
        },
        
    }
}
</script>

<style scoped lang="less">
    .warpper{
        // width: 100%;
        // height: 100%;
        // overflow: hidden;
        .menu{
            // line-height: 20px;
            // vertical-align: middle
            padding: 10px 0 10px 0
        }
    }



</style>
