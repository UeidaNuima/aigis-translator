<template>
  <div id="app">
    <div class="menu">
      <div class="logo inline-block">
        <a href="/">千年翻译个狗</a>
      </div>
      <div class="inline-block input-container">
        <el-input v-model="name" placeholder="你是谁?">
          <el-button type="primary" slot="append" @click="saveName">对</el-button>
        </el-input>
      </div>
    </div>
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  name: 'app',
  data() {
    return {
      name: '',
    };
  },
  methods: {
    saveName() {
      localStorage.setItem('name', this.name);
      if (this.name !== '') {
        this.$message({
          message: `好的你现在是${this.name}了`,
          type: 'success',
        });
      } else {
        this.$message({
          message: '好的你现在是咕咕咕咕咕咕咕咕咕了',
          type: 'success',
        });
      }
    },
  },
  created() {
    this.name = localStorage.getItem('name') || '';
  },
};
</script>


<style scoped>
#app {
  /* height: calc(100% - 50px); */
  padding-top: 50px;
}
.menu {
  background-color: #20A0FF; 
  position: fixed;
  top: 0;
  width: 100%;
  z-index: 100;
}
.logo {
  height: 50px;
  line-height: 50px;
  
  font-size: 1.2em;
  margin-left: 30px;
}
.logo a {
  color: #FFFFFF;
  text-decoration: none;
}

.inline-block {
  display: inline-block;
}
.input-container {
  margin-left: 50px;
  width: 150px;
}
</style>

<style>
html {
  height: 100%;
}
body {
  margin: 0;
  background-color: #E5E9F2;
  height: 100%;
}
</style>
