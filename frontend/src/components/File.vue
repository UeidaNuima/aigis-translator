<template>
  <el-row>
    <el-col :span="6" class="full-height-cutting-menu toc" v-if="file.type === 'atb'">
      <el-menu default-active="0">
        <el-menu-item-group :title="file.name">
          <el-menu-item
            v-for="(field, index) in file.data"
            v-if="index >= (page - 1) * 100 && index < page * 100"
            :index="String(index)" 
            :key="field.origin"
            :class="{
              'translated': file.data[index].translation,
              'submitted': file.data[index].translator_ip,
            }"
            @click="activate(index)">
            {{ index + 1 }} - {{ field.origin }}
          </el-menu-item>
        </el-menu-item-group>
      </el-menu>
      <el-pagination
        small
        layout="total, prev, next, jumper"
        :page-size="100"
        :total="file.data.length"
        :current-page="page"
        @current-change="handleCurrentChange">
      </el-pagination>
    </el-col>
    <el-col :span="file.type === 'atb'? 18 : 24" class="full-height-cutting-menu">
      <div class="full-height">
        <el-row class="full-height-cutting-tool-bar">
          <el-col :span="12" class="full-height">
            <textarea
              class="tranlation-textarea"
              placeholder="请把翻译内容写在这儿"
              v-model="file.data[activatedIndex].translation"></textarea>
          </el-col>
          <el-col :span="12" class="full-height">
            <div class="origin">
              <pre>{{ file.data[activatedIndex].origin }}</pre>
            </div>
          </el-col>
        </el-row>
        <div class="tool-bar">
          <el-button type="primary" @click="submit">提交翻译</el-button>
          翻译者信息: {{ file.data[activatedIndex].translator_name }}/{{ file.data[activatedIndex].translator_ip }}
        </div>
      </div>
      <div class="info-panel">

      </div>
    </el-col>
  </el-row>
</template>

<script>

import { Loading } from 'element-ui';

export default {
  name: 'file',
  data() {
    return {
      id: '',
      file: {
        data: [{}],
      },
      activatedIndex: 0,
      loading: true,
      page: 1,
    };
  },
  computed: {
    totalPage() {
      return Math.ceil(this.file.data.length / 100);
    },
  },
  methods: {
    activate(index) {
      this.activatedIndex = index;
    },
    init() {
      const loadingInstance = Loading.service({ fullscreen: true });
      this.$http.get('file_raw', {
        params: {
          id: this.$route.params.id,
        },
      })
        .then((response) => {
          this.file = response.data;
          loadingInstance.close();
        });
    },
    submit() {
      Loading.service({ fullscreen: true });
      this.$http.put('file_raw', {
        translation: this.file.data[this.activatedIndex].translation,
        index: this.activatedIndex,
        translator_name: localStorage.getItem('name'),
      }, {
        params: {
          id: this.$route.params.id,
        },
      })
        .then(() => {
          this.init();
        });
    },
    handleCurrentChange(val) {
      this.page = val;
    },
  },
  created() {
    this.init();
  },
};
</script>

<style scoped>
.full-height-cutting-menu {
  height: calc(100vh - 50px);
}
.full-height {
  height: 100%;
}
.full-height-cutting-tool-bar {
  height: calc(100% - 80px);
}
.toc {
  background-color: #eef1f6;
  overflow-y: scroll;
  overflow-x: hidden;
}
.tranlation-textarea {
  resize: none;
  height: calc(100% - 40px);
  width: calc(100% - 40px);
  margin: 0;
  padding: 20px;
  border: none;
  background-color: white;
  display: block;
}

.tranlation-textarea:focus {
  outline: none;
}
.origin {
  background-color: #ffffff;
  padding: 20px;
  height: calc(100% - 40px);
  border-left: 1px dashed #324057;
  overflow: auto;
}
.tool-bar {
  height: 39px;
  line-height: 40px;
  padding: 20px;
  background-color: #324057;
  color: #ffffff;
}
.translated {
  background-color: #F7F29C;
}
.submitted {
  background-color: #9CF7C4;
}
pre {
  margin: 0;
}
</style>