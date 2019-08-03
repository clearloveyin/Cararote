<template>
    <div id="man-day-container" @mousewheel.prevent @click.stop.prevent @mousedown.stop>
        <slot></slot>
        <i class="arrow" :class="activeArrow"></i>
    </div>
</template>
<script>
export default {
    name: 'manDayDialog',
    props: {
        selectedArea: {
            type: Object,
            default() {
                return {}
            }
        },
        dialogWidth: {
            type: Number,
            default: 200
        },
        dialogHeight: {
            type: Number,
            default: 500
        }
    },
    data() {
        return {
            activeArrow: ''
        }
    },
    watch: {
        selectedArea(value) {
            this.calculatemanDayPosition()
        }
    },
    methods: {
        calculatemanDayPosition() {
            const clientWidth = document.body.offsetWidth
            const clientHeight = document.body.offsetHeight
            const manDayWidth = this.dialogWidth  + 40
            const manDayHeight = this.dialogHeight + 40
            const tdWidth = Number(this.selectedArea.width)
            const tdHeight = Number(this.selectedArea.height)
            const tdTop = Number(this.selectedArea.top)
            const tdLeft = Number(this.selectedArea.right)

            let leftInstance
            let topInstance
            let manDayStyle
            function setLeftStyle(value) {
                return 'left: ' + value + 'px;'
            }
            function setTopStyle(value) {
                return 'top: ' + value + 'px;'
            }
            if (clientWidth >= tdLeft + manDayWidth) {
                //浏览器宽度 大于 指摘+定位总宽度
                leftInstance = setLeftStyle(tdLeft + 8)
                if (clientHeight >= tdTop + manDayHeight) {
                    //浏览器高度 大于 指摘+定位总高度
                    topInstance = setTopStyle(tdTop)
                    this.activeArrow = 'arrow-left-top'
                } else {
                    //浏览器高度 小于 指摘+定位总高度
                    if (manDayHeight >= tdTop) {
                        //指摘高度 大于 td top
                        topInstance = setTopStyle(tdTop)
                        this.activeArrow = 'arrow-left-top'
                    } else {
                        topInstance = setTopStyle(tdTop - manDayHeight + tdHeight)
                        this.activeArrow = 'arrow-left-bottom'
                    }
                }
            } else {
                //浏览器宽度 大于 指摘+定位总宽度
                console.log(tdLeft, manDayWidth, tdWidth)
                leftInstance = setLeftStyle(tdLeft - manDayWidth)
                if (clientHeight >= tdTop + manDayHeight) {
                    //浏览器高度 大于 指摘+定位总高度
                    topInstance = setTopStyle(tdTop + tdHeight)
                    this.activeArrow = 'arrow-top-right'
                } else {
                    //浏览器高度 小于 指摘+定位总高度
                    if (manDayHeight >= tdTop) {
                        //指摘高度 大于 td top
                        topInstance = setTopStyle(tdTop - 8)
                        this.activeArrow = 'arrow-right-top'
                    } else {
                        topInstance = setTopStyle(tdTop - manDayHeight + tdHeight)
                        this.activeArrow = 'arrow-right-bottom'
                    }
                }
            }
            let manDayContentDom = document.getElementById('man-day-container')
            manDayStyle = leftInstance + topInstance + 'width: ' + this.dialogWidth + 'px;' + 'height: ' + this.dialogHeight + 'px;'
            manDayContentDom.style = manDayStyle
        }
    }
}
</script>
<style scoped>
#man-day-container {
    position: fixed;
    left: 361px;
    top: 350px;
    /* width: 200px;
    height: 100px; */
    background-color: #fff;
    filter: drop-shadow(0 3px 5px black);
    padding: 18px 20px;
    z-index: 20000;
    text-align: left;
}
.arrow {
    position: absolute;
    width: 0;
    height: 0;
    overflow: hidden;
    border: 7px solid transparent;
}

.arrow-left-top {
    left: -14px;
    top: 8px;
    border-right-color: #fff;
}
.arrow-left-bottom {
    left: -14px;
    top: 316px;
    border-right-color: #fff;
}
.arrow-right-top {
    left: 280px;
    top: 8px;
    border-left-color: #fff;
}
.arrow-top-right {
    left: 218px;
    top: -14px;
    border-bottom-color: #fff;
}
.arrow-right-bottom {
    left: 280px;
    top: 316px;
    border-left-color: #fff;
}
</style>