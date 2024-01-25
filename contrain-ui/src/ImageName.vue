<template>
  <div class="config-form-body">
    <div class="ImageName">
    <h2 class="config_title">图片重命名工具</h2>
      <form @submit.prevent="handleSubmit">
        <div class="prabox">
          <div>
            <div class="praen">image_path</div>
            <div class="pracn">
              <label for="imageDir">图片文件夹路径</label>
            </div>
            <input class="input_box" id="imageDir" v-model="modelPaths.imageDir" type="text">
          </div>
          <div class="button-name">
            <button class="button-in-name" type="submit">开始批量重命名</button>
          </div>
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

.ImageName{
  width: 86%;
  max-width: 900px;
  margin: 20px auto;
  padding: 0 10px;
  padding: 20px;
  margin: 10px 0;
  box-sizing: border-box;
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

.button-name {
    display: flex;
    justify-content: space-between;
    padding: 20px 0;
  }

  .button-name button {
    flex: 1;
    margin-right: 10px;
    background-color: #e0e0e0;
    border: none;
    box-shadow: 4px 4px 8px #e8e8e8, -4px -4px 8px #ffffff;
    color: rgb(255, 255, 255);
  }

  .button-name button:last-child {
    margin-right: 0;
  }

  .button-in-name {
    padding: 12px 25px;
    border: 1px solid transparent;
    border-radius: 12px;
    background-image: linear-gradient(to right, #b0c3ff, #8f94fb);
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

  .button-in-name:hover, .button-in-name:focus {
    background-image: linear-gradient(to left, #8f94fb, #4e54c8);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
    border-color: #8f94fb;
  }

  .button-in-name:active {
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
            imageDir: '',
        }
      };
    },
    methods: {
      handleSubmit() {
        const imageDirPaths = {
            imageDir: this.imageDirPaths(this.modelPaths.imageDir),
        };
        console.log(imageDirPaths.imageDir); // 这将在浏览器的控制台中显示组合后的路径
  
        // 发送规范化的路径到后端
        this.submitPaths(imageDirPaths);
      },
      imageDirPaths(path) {
        // 将路径中的反斜杠转换为正斜杠
        return path.replace(/\\/g, '/');
      },

      async submitPaths(paths) {
        try {
          // 发送请求到后端 API
          const response = await fetch('http://localhost:3000/update-image-yaml', {
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
          await fetch('http://localhost:3000/named-script', { method: 'POST' });
        } catch (error) {
          console.error('Error:', error);
        }
      }
    }
  };
</script>