<template>
  <div class="config-form-body">
    <div class="ModelLocal">
      <h2 class="config_title">模型预处理</h2>
      <form @submit.prevent="handleSubmit">
        <div class="prabox">
          <div class="praen">model_path</div>
          <div class="pracn">
            <label for="inputModelPath">输入参考模型路径</label>
          </div>
          <input class="input_box" id="inputModelPath" v-model="modelPaths.inputModelPath" type="text">
        </div>
        <div class="prabox">
          <div class="praen">out_model_path</div>
          <div class="pracn">
            <label for="outputModelPath">输出路径</label>
          </div>
          <input class="input_box" id="outputModelPath" v-model="modelPaths.outputModelPath" type="text">
        </div>
        <div class="prabox">
          <div class="praen">model_name</div>
          <div class="pracn">
            <label for="outputModelName">新模型名字</label>
          </div>
          <input class="input_box" id="outputModelName" v-model="modelPaths.outputModelName" type="text">
        </div>
        <div class="button-container">
          <button class="button-in" type="submit">开始生成空白模型</button>
        </div>
      </form>
    </div>
  </div>
</template>

<style>
.config-form-body{
  width: auto;
  display: flex; /* 使用flexbox布局 */
  flex-direction: column; /* 子元素垂直排列 */
  align-items: center; /* 子元素在交叉轴上（水平方向）居中 */
  justify-content: center; /* 子元素在主轴上（垂直方向）居中，如果你也想要垂直居中的话 */
}

.config_title {
    font-family: 'Roboto', sans-serif;
    text-align: center;
    color: rgb(51, 51, 51);
    margin: 20px 0;
    padding: 10px 0;
    display: inline-block;
    font-size: 2em;
    transition: transform 0.3s ease;
  }

.ModelLocal {
    width: 86%;
    max-width: 900px;
    margin: 20px auto;
    padding: 0 10px;
    padding: 20px;
    margin: 10px 0;
    box-sizing: border-box;
  }

  .praen {
    margin: 5px 0;
  }

  .pracn {
    margin: 5px 0;
  }

  form input[type="text"],
  form input[type="number"],
  form select,
  form button {
    width: 100%;
    box-sizing: border-box;
    margin-bottom: 10px;
    background-color: #f8f8f8;
    box-shadow: 8px 8px 16px #eaeaea, -8px -8px 16px #ffffff; 
    box-shadow: 8px 8px 16px #eaeaea, -8px -8px 16px #ffffff; 
    color: rgb(73, 73, 73);
  }

  .input_box {
    width: 100%;
    padding: 10px 15px;
    margin: 5px 0 15px 0;
    border: 1px solid rgb(234, 234, 234);
    border-radius: 12px;
    background-color: white;
    font-size: 16px;
    transition: border-color 0.3s ease-in-out;
  }

  .input_box:focus {
    border-color: #80bdff;
    outline: none;
    box-shadow: 0 0 0 2px rgba(0, 123, 255, 0.25);
  }

  .input_box[type="checkbox"] {
    width: auto;
    margin: 10px 0;
    padding: 0;
    border: none;
    background-color: transparent;
  }

  .input_box:hover {
    border-color: #66afe9;
  }

  .prabox {
    border-bottom: 1px solid #ccc;
    padding-bottom: 10px;
    margin-bottom: 10px;
  }

  .prabox:first-child {
    border-top: 1px solid #ccc;
  }

  .prabox:last-child {
    border-bottom: none;
  }

  .button-container {
    display: flex;
    justify-content: space-between;
    padding: 20px 0;
  }

  .button-container button {
    flex: 1;
    margin-right: 10px;
    background-color: #e0e0e0;
    border: none;
    box-shadow: 4px 4px 8px #e8e8e8, -4px -4px 8px #ffffff;
    color: rgb(255, 255, 255);
  }

  .button-container button:last-child {
    margin-right: 0;
  }

  .button-in {
    padding: 12px 25px;
    border: 1px solid transparent;
    border-radius: 12px;
    background-image: linear-gradient(to right, #003cff, #4d73ff);
    color: white;
    font-family: 'Helvetica Neue', sans-serif;
    font-size: 16px;
    font-weight: bold;
    cursor: pointer;
    outline: none;
    box-shadow: 
      0 2px 4px rgba(134, 153, 211, 0.726),
      inset 2px 6px 2px rgba(255, 255, 255, 0.836), /* 内阴影为按钮添加一些立体感 */
      inset -2px -6px 2px rgba(0, 0, 0, 0.6); /* 内阴影为按钮添加深度感 */
    transition: all 0.3s ease;
    text-transform: uppercase;
    letter-spacing: 1px;
  }

  .button-in:hover, .button-in:focus {
    background-image: linear-gradient(to left, #8f94fb, #4e54c8);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
    border-color: #8f94fb;
  }

  .button-in:active {
    transform: translateY(1px);
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
  }

</style>

<script>
// import axios from 'axios';

export default {
  data() {
    return {
      modelPaths: {
        inputModelPath: '',
        outputModelPath: '',
        outputModelName: '',
      }
    };
  },
  
  methods: {
    handleSubmit() {
      // 组合输出模型路径和模型名字
      const combinedOutputPath = this.combinePaths(
        this.modelPaths.outputModelPath,
        this.modelPaths.outputModelName
      );
      const normalizedPaths = {
        inputModelPath: this.normalizePath(this.modelPaths.inputModelPath),
        combinedOutputPath: this.normalizePath(combinedOutputPath),
      };
      console.log(normalizedPaths.combinedOutputPath); // 这将在浏览器的控制台中显示组合后的路径

      // 发送数据到后端
      this.submitPaths(normalizedPaths);
    },
    normalizePath(path) {
      // 将路径中的反斜杠转换为正斜杠
      return path.replace(/\\/g, '/');
    },
    combinePaths(path, name) {
      // 确保路径以斜杠结尾
      if (path[path.length - 1] !== '/') {
        path += '/';
      }
      // 返回组合后的完整路径
      return path + name + '.ckpt';
    },
    async submitPaths(paths) {
      try {
        // 发送请求到后端 API
        const response = await fetch('http://localhost:3000/update-model-paths', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(paths)
        });

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        // 触发 tool_add_control.py 脚本的执行
        await fetch('http://localhost:3000/trigger-script', { method: 'POST' });
      } catch (error) {
        console.error('Error:', error);
      }
    }
  }
};
</script>