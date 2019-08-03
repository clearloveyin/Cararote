<template>
    <div class="warpper">
        <div class="content">
            <h3>{{title}}(Input资料)</h3>
            <h5>版本：{{version}}</h5>
            <div class="content-text text-style" v-html="content">{{content}}</div>
        </div>        
    </div>
</template>

<script>
export default {
    data() {
        return {
            title:"标题",
            content:'',
            version:""
        }
    },
    mounted() {
        this.default_mounted()
    },
    methods: {
        default_mounted(){
            let data = JSON.parse(sessionStorage.getItem('input_version_data'))
            this.content = data.url
            this.version = data.version_id
            this.title = data.name
        },
        
    }
}
</script>

<style scoped lang="less">
    *{
        margin: 0;
        padding: 0
    }
    .warpper{
        width: 100%;
        height: 100%;
        color: #5e6d82;
        overflow: hidden;
        h3,h5{
            padding-top:10px
        }
        .content{
            margin: 30px auto;
            text-align: center
        }
        .content-text{
            width: 720px;
            margin: 0 auto;
            padding: 20px 0 0;
            font-size: 14px;
        }
        .text-style{
            line-height: 28px;
            white-space: normal;

        }
        .text-style::after{
            content: "";
            display: inline-block;
            padding-left: 100%
        }

    }


</style>
