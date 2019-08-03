<template>
    <header class="header">
        <div class="left logo">
            Spider
        </div>
    </header>
</template>
<style lang="scss" scoped>
    $height:60px;
    $fontSize:22px;
    .header{
        // width: 100%;
        height: $height;
        background: #444;
        color: white;
        .left{
            // display: inline-block;
            height: $height;
            line-height: $height;
            float: left;
        }
        .logo{
            font-size: $fontSize;
            font-weight: bold

        }
    }
</style>
