<template>
  <div class="warpper">
    <div class="tab-content-first">
      <ul class="tab-content-first-ul">
        <li
          class="asa-li"
          v-for="item in tab_list_data"
          :key="item.name"
          @click="tab_box_click_fun(item)"
        >
          <div class="content-size-box">
            <p class="tab-content-size tab-content-size-ex">{{item.name}}</p>
          </div>
          <div class="Asa-box">
            <ul
              class="tab-content-first-ul tab-content-ul-column"
              v-for="children in item.list"
              :key="children.name"
            >
              <li @click='tab_box_children_click_fun(children)'>
                <div class="content-size-box content-size-box-ex">
                  <p class="tab-content-size tab-content-size-ex tab-content-ex">{{children.children_name}}</p>
                </div>
              </li>
            </ul>
          </div>
        </li>
      </ul>
    </div>

    <footer>Copyright&nbsp;&copy;&nbsp;2018 iAUTO</footer>
  </div>
</template>

<script>
export default {
  name: 'tab',
  data () {
    return {
      user_name: '',
      page: 1,
      page_size: 20,
      tab_list_data: [
        { name: '工数' },
        { name: 'INPUT资料' },
        { name: '项目' },
        {
          name: '管理',
          list: [
            { children_name: '平台管理' },
            { children_name: '项目管理' },
            { children_name: '模块信息管理' },
            { children_name: '模块关系管理' },
            // {children_name:'式样书管理'},
            { children_name: '用户管理' },
            { children_name: '角色/权限管理' }
          ]
        }
      ]
    }
  },
  mounted () {
    this.user_name = window.sessionStorage.getItem('Uall')
    // console.log(this.userPurviewManage("平台管理"))
  },
  methods: {
    tab_box_click_fun (val) {
      switch (val.name) {
        case '工数':
          // this.go_development_book()
          break
        case 'INPUT资料':
          this.go_to_input_data_fun()
          break
        case '项目':
          this.go_to_project_fun()
          break
        default:
          break
      }
    },
    go_to_input_data_fun () {
      this.$router.push('/Input/InputList')
    },
    go_to_project_fun () {
      this.$router.push('/proj/proj_content')
    }
  }
}
</script>

<style scoped >
* {
  margin: 0;
  padding: 0;
}
html,
body {
  font-family: "微软雅黑";
  /*font-size: 14px;*/
}
a {
  text-decoration: none;
}
ul,
ol,
li {
  list-style: none;
}
header span u {
  font-size: 14px;
}
.fl {
  float: left;
}
.fr {
  float: right;
}
.warpper {
  position: absolute;
  width: 100%;
  height: 100%;
  /* background: url('../../assets/image/homepageimage.jpg') no-repeat; */
  background-size: 100% 100%;
  background-color: #f5e7d7;
}
header1 {
  width: 100%;
  height: 60px;
  position: fixed;
  top: 0;
  left: 0;
  /*	background: #f8fafc;*/
  box-shadow: 3px 0 5px #dedede;
  -webkit-box-shadow: 3px 0 5px #dedede;
  line-height: 60px;
}
.hmi-size {
  display: block;
  margin: 19px 0 0 20px;
  font-weight: 600;
  font-size: 24px;
  color: #42b983;
  /* background: url('../assets/img/tab_log.png') no-repeat; */
  background-size: 100% 100%;
  width: 106px;
  height: 23px;
}
footer {
  width: 100%;
  height: 60px;
  position: fixed;
  bottom: 0;
  left: 0;
  /*	background: #f8fafc;*/
  line-height: 60px;
  color: #93999f;
  font-size: 12px;
  text-align: center;
  box-shadow: -3px 0 5px #dedede;
  -webkit-box-shadow: -3px 0 5px #dedede;
}

.fl {
  float: left;
}
.fr {
  float: right;
}

.tab-content-first {
  position: absolute;
  width: 100%;
  height: 114px;
  top: 40%;
  margin-top: -57px;
  left: 0;
  z-index: 10;
}
.tab-content-first-ul {
  width: 90%;
  min-width: 1024px;
  margin: 0 auto;
  /*background: #fff;*/
  display: flex;
  justify-content: space-around;
}
.tab-content-ul-column {
  width: 234px;
  min-width: 234px;
  flex-direction: column;
}
.tab-content-first-ul li {
  width: 234px;
  height: 114px;
  cursor: pointer;
  border-radius: 5px;
  position: relative;
  background: hsla(0, 0%, 100%, 0.3);
  transition: all 0.5s linear;
  -moz-transition: all 0.5s linear; /* Firefox 4 */
  -webkit-transition: all 0.5s linear; /* Safari 和 Chrome */
  -o-transition: all 0.5s linear;
  /* background: url('../assets/img/tab_small_show.png') no-repeat; */
  background-size: 100% 100%;
}
.tab-content-first-ul li:hover {
  box-shadow: 0 0 0 1px hsla(0, 52%, 36%, 0.3) inset,
    0 0.5em 1em rgba(0, 0, 0, 0.6);
  text-shadow: 0 1px 1px hsla(0, 6%, 16%, 0.3);
  /* background: url('../assets/img/tab_small_hidden.png') no-repeat; */
  background-size: 100% 100%;
  background: hsla(0, 0%, 100%, 0.3);
}
.Asa-box .tab-content-first-ul li:hover {
  box-shadow: none;
}
.Asa-box .tab-content-first-ul li:hover .content-size-box .tab-content-ex {
  color: #333;
}
.tab-content-first-ul li:hover .content-size-box .tab-content-ex {
  color: #42b983;
}

.tab-content-first-ul li:hover .content-size-box p {
  color: #333;
}
.tab-content-first-ul li .content-size-box p {
  width: 160px;
  padding-left: 35px;
  height: 20px;
  line-height: 20px;
  color: #42b983;
  font-size: 24px;
}
.Asa-box .tab-content-first-ul li .content-size-box p {
  font-size: 14px;
}
.tab-content-size {
  font-weight: 500;
}
.content-size-box {
  margin-top: 36px;
}
.content-size-box-ex {
  margin-top: 0;
}
.tab-content-first-ul li .content-size-box .tab-content-size-ex {
  height: 47px;
  line-height: 47px;
}

.asa-li {
  position: relative;
}
.asa-li:hover .Asa-box {
  display: inline-block;
}
.Asa-box {
  position: absolute;
  left: 10px;
  top: 114px;
  width: 210px;
  display: none;
}

@media only screen and (max-width: 1440px) {
  .Asa-box .tab-content-first-ul li .content-size-box p {
    font-size: 12px;
  }
  .tab-content-first-ul {
    width: 100%;
    min-width: 936px;
    margin: 0 auto;
    /*background: #fff;*/
    display: flex;
    justify-content: space-around;
  }
  .tab-content-first-ul li {
    width: 205px;
    height: 100px;
    cursor: pointer;
    border-radius: 5px;
    position: relative;
    background: hsla(0, 0%, 100%, 0.3);
    transition: all 0.5s linear;
    -moz-transition: all 0.5s linear; /* Firefox 4 */
    -webkit-transition: all 0.5s linear; /* Safari 和 Chrome */
    -o-transition: all 0.5s linear;
    /* background: url('../assets/img/tab_small_show.png') no-repeat; */
    background-size: 100% 100%;
  }
  .tab-content-first-ul li .content-size-box p {
    width: 150px;
    padding-left: 30px;
    height: 20px;
    line-height: 20px;
    color: #42b983;
    font-size: 16px;
  }
  .content-size-box {
    margin-top: 28px;
  }
  .Asa-box {
    position: absolute;
    left: 10px;
    top: 100px;
    display: none;
  }
  .asa-li .Asa-box .tab-content-first-ul li {
    margin-top: 11px;
    height: 40px;
    width: 180px;
  }
  .content-size-box-ex {
    margin-top: 0;
  }
  .tab-content-ul-column {
    width: 164px;
    min-width: 164px;
    flex-direction: column;
    margin: 0;
  }
  .tab-content-first-ul li .content-size-box .tab-content-size-ex {
    height: 42px;
    line-height: 42px;
  }
}

@media only screen and (max-width: 1280px) {
  .Asa-box .tab-content-first-ul li .content-size-box p {
    font-size: 12px;
  }
  .tab-content-first-ul {
    width: 100%;
    min-width: 936px;
    margin: 0 auto;
    /*background: #fff;*/
    display: flex;
    justify-content: space-around;
  }
  .tab-content-first-ul li {
    width: 164px;
    height: 80px;
    cursor: pointer;
    border-radius: 5px;
    position: relative;
    background: hsla(0, 0%, 100%, 0.3);
    transition: all 0.5s linear;
    -moz-transition: all 0.5s linear; /* Firefox 4 */
    -webkit-transition: all 0.5s linear; /* Safari 和 Chrome */
    -o-transition: all 0.5s linear;
    /* background: url('../assets/img/tab_small_show.png') no-repeat; */
    background-size: 100% 100%;
  }
  .tab-content-first-ul li .content-size-box p {
    width: 150px;
    padding-left: 10px;
    height: 20px;
    line-height: 20px;
    color: #42b983;
    font-size: 15px;
  }
  .content-size-box {
    margin-top: 15px;
  }
  .Asa-box {
    position: absolute;
    left: 10px;
    top: 80px;
    display: none;
  }
  .asa-li .Asa-box .tab-content-first-ul li {
    margin-top: 11px;
    height: 40px;
    width: 150px;
  }
  .content-size-box-ex {
    margin-top: 0;
  }
  .tab-content-ul-column {
    width: 164px;
    min-width: 164px;
    flex-direction: column;
    margin: 0;
  }
  .tab-content-first-ul li .content-size-box .tab-content-size-ex {
    height: 42px;
    line-height: 42px;
  }
}

.Asa-box .tab-content-first-ul li {
  margin-top: 11px;
  height: 50px;
  width: 217px;
  /* background: url('../assets/img/tab_hidden_small.png') no-repeat; */
  background-size: 100% 100%;
}

.Asa-box .tab-content-first-ul li:hover {
  /* background: url('../assets/img/tab_show_small.png') no-repeat; */
  background-size: 100% 100%;
}
.Asa-box .tab-content-first-ul li:hover p {
  color: white;
}
/* .Asa-box .tab-content-first-ul li:hover {
    box-shadow: 0 0 0 1px hsla(0, 0%, 100%, 0.3) inset, 0 0.5em 1em rgba(0, 0, 0, 0.6);
    text-shadow: 0 1px 1px hsla(0, 0%, 100%, 0.3);
    background: hsla(0, 0%, 100%, 0.3);
} */
/* .Asa-box .tab-content-first-ul li:hover .content-size-box p {
    color: black;
} */
</style>
