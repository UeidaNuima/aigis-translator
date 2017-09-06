<template>
  <div class="container">
    <el-tree
      :data="files"
      :render-content="renderContent"
      v-loading="loading"
      lazy
      :props="{ label: 'name', children: 'children'}"
      :load="loadNode"
      @node-click="nodeClickHandler"
      ></el-tree>
  </div>
</template>

<script>
import moment from 'moment';

moment.locale('zh-cn');

export default {
  name: 'main',
  data() {
    return {
      files: [],
      loading: false,
    };
  },
  methods: {
    renderContent(h, { node, data }) {
      const percentage = parseInt(data.percentage_translated * 100, 10) || 0;
      return (
        <span>
          <span>
            <span>{ node.label } / { moment(data.time_stamp).fromNow() }</span>
          </span>
          <el-progress v-show={ data.type !== 'aar' } class="progress-bar" text-inside={ true } stroke-width={ 18 } percentage={ percentage }></el-progress>
        </span>
      );
    },
    nodeClickHandler(data) {
      if (data.type !== 'aar') {
        this.$router.push(`/file/${data.id}`);
      }
    },
    loadNode(node, resolve) {
      this.loading = true;
      this.$http.get('file_list', {
        params: {
          level: node.level,
          id: node.data.id,
        },
      })
        .then((response) => {
          this.loading = false;
          resolve(response.data);
        });
      resolve([]);
    },
  },
  created() {
    // this.$http.get('file_list')
    //   .then((response) => {
    //     this.files = response.data;
    //     this.loading = false;
    //   });
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.container {
  margin: 10px;
  padding: 20px;
  background-color: #FFFFFF;
  /* height: calc(100% - 60px); */
}
</style>

<style>
.progress-bar {
  width: 300px;
  float: right;
  margin-top: 9px;
  margin-right: 20px;
}
</style>
