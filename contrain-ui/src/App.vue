<template>
  <div id="app" class="container">
    <!-- 左侧边栏 -->
    <div class="left-sidebar">
      <div class="left-sidebar-block">
        <ul class="left-sidebar-box">
          <div class="left-sidebar-box-option"
              :class="{ 'active': activeComponent === 'Toolbox' }"
              @click="setActiveComponent('Toolbox')"
              @mouseenter="hovered = 'Toolbox'"
              @mouseleave="hovered = ''">
            <li>小工具</li>
            <div class="note_dot_nothing"></div>
            <div class="note_dot" v-show="activeComponent === 'Toolbox' || hovered === 'Toolbox'"></div>
          </div>
          <div class="left-sidebar-box-option"
              :class="{ 'active': activeComponent === 'ModelLocal' }"
              @click="setActiveComponent('ModelLocal')"
              @mouseenter="hovered = 'ModelLocal'"
              @mouseleave="hovered = ''" >
            <li>模型预处理</li>
            <div class="note_dot_nothing"></div>
            <div class="note_dot" v-show="activeComponent === 'ModelLocal' || hovered === 'ModelLocal'"></div>
          </div>
          <div class="left-sidebar-box-option"
              :class="{ 'active': activeComponent === 'ConfigForm' }"
              @click="setActiveComponent('ConfigForm')"
              @mouseenter="hovered = 'ConfigForm'"
              @mouseleave="hovered = ''">
            <li>训练模型</li>
            <div class="note_dot_nothing"></div>
            <div class="note_dot" v-show="activeComponent === 'ConfigForm' || hovered === 'ConfigForm'"></div>
          </div>
        </ul>
        <div class="sign-nothing"></div>
        <div class="sign-box">
          <a href="https://space.bilibili.com/523893438?spm_id_from=333.999.0.0" target="_blank" class="sign-box-link">
          controlnet
          </a>
        </div>
      </div>
    </div>

    <div class="content">
        <ImageName v-if="activeComponent === 'Toolbox'" @submit="handleSubmit"/>
        <PromptCreate v-if="activeComponent === 'Toolbox'" @submit="handleSubmit"/>
        <ModelLocal v-if="activeComponent === 'ModelLocal'" @submit="handleSubmit"/> 
        <ConfigForm v-if="activeComponent === 'ConfigForm'" @submit="handleSubmit"/>
    </div>
        <!-- 右侧边栏 -->
    <div class="right-sidebar">
      <div class="right-box">
          <div class="right-sidebar-up">
            <h2>训练流程</h2>
            <a class="train_line">1. 制作训练集，准备原始鱼片、条件图片与目标图片；</a>
            <a class="train_line">2. 条件图片放到“source”文件夹中，目标图片放到“target”文件夹中（文件夹的命名一定要非常准确）；</a>
            <a class="train_line">3. 使用小工具制作prompt.js文件；</a>
            <a class="train_line">4. 将sd模型进行预处理；</a>
            <a class="train_line">5. 输入参数进行训练；</a>
            <a class="train_line">6. 训练完毕进行检验。</a>
          </div>
          <div class="right-sidebar-down">
            <div class="right-box">
              <h2 class="train_par_content_title">训练参数详解</h2>
              <div class="train_par_content_box" @scroll="handleScroll">
                <div id="pretrained_model_path" class="train_par_content">
                  <a class="train_par_content_at">pretrained_model_path（预训练模型位置）</a>
                  <a class="train_par_content_ac">将模型预处理产生的新模型的位置放到这里</a>
                </div>
                <div id="training_set_path" class="train_par_content">
                  <a class="train_par_content_at">training_set_path（训练集文件夹）</a>
                  <a class="train_par_content_ac">将source和target的根目录的文件路径放到这</a>
                </div>
                <div id="SD_Locked" class="train_par_content">
                  <a class="train_par_content_at">SD_Locked（SD锁定）</a>
                  <a class="train_par_content_ac">不勾选时将训练Decoder层，默认勾选以避免数据集质量低影响模型性能</a>
                </div>
                <div id="only_mid_control" class="train_par_content">
                  <a class="train_par_content_at">only_mid_control（仅训练中间层）</a>
                  <a class="train_par_content_ac">勾选时训练的架构将只在中间层，而不是整体，速度较快，资源占用较低</a>
                </div>
                <div id="batch_size" class="train_par_content">
                  <a class="train_par_content_at">batch_size（并行训练数量）</a>
                  <a class="train_par_content_ac">一次训练几张图片，低显存勿勾</a>
                </div>
                <div id="save_every_n_epochs" class="train_par_content">
                  <a class="train_par_content_at">save_every_n_epochs（每几轮保存一次）</a>
                  <a class="train_par_content_ac">一次训练几张图片，低显存勿勾</a>
                </div>
                <div id="accumulate_grad_batches" class="train_par_content">
                  <a class="train_par_content_at">accumulate_grad_batches（累计梯度批次）</a>
                  <a class="train_par_content_ac">加快训练速度，效果几乎等于batch_size，但是不实际增加显存</a>
                </div>
                <div id="num_workers" class="train_par_content">
                  <a class="train_par_content_at">num_workers（并行处理进程）</a>
                  <a class="train_par_content_ac">多进程加载数据，电脑性能不足的话一定设为0</a>
                </div>
                <div id="max_epochs" class="train_par_content">
                  <a class="train_par_content_at">max_epochs（最大训练轮数）</a>
                  <a class="train_par_content_ac">数据集里的数据被整体的学习了一轮，这个过程总共会进行几轮</a>
                </div>
                <div id="repeats" class="train_par_content">
                  <a class="train_par_content_at">repeats（每轮中数据重复训练次数）</a>
                  <a class="train_par_content_ac">在一个epoch中，数据集里的数据被重复训练的次数</a>
                </div>
                <div id="shuffle" class="train_par_content">
                  <a class="train_par_content_at">shuffle（随机数据集顺序）</a>
                  <a class="train_par_content_ac">将数据集里的数据随机进行训练</a>
                </div>
                <div id="save_every_n_epochs" class="train_par_content">
                  <a class="train_par_content_at">save_every_n_epochs（每几轮保存一次）</a>
                  <a class="train_par_content_ac">max_epochs除以此参数等于你最后会得到几个模型</a>
                </div>
                <div id="precision" class="train_par_content">
                  <a class="train_par_content_at">precision（训练精度）</a>
                  <a class="train_par_content_ac">训练模型时使用的数值精度，30系及以上显卡推荐bf16</a>
                </div>
                <div id="optimizer" class="train_par_content">
                  <a class="train_par_content_at">optimizer（优化器）</a>
                  <a class="train_par_content_ac">定义更新模型的权重的方式、学习速度</a>
                </div>
                <div id="d_coef" class="train_par_content">
                  <a class="train_par_content_at">d_coef（学习率估计系数）</a>
                  <a class="train_par_content_ac">搭配“Prodigy”使用的参数，用于影响学习率估计的系数。默认为1.0。值大于1会导致估计更大的学习率，而小于1的值会导致较小的学习率</a>
                </div>
                <div id="safeguard_warmup" class="train_par_content">
                  <a class="train_par_content_at">safeguard_warmup（预热防护）</a>
                  <a class="train_par_content_ac">在调度器选择“常量预热 / constant_warmup”的时候建议开启，防止过度调整学习率</a>
                </div>                
                <div id="Learning_rate" class="train_par_content">
                  <a class="train_par_content_at">Learning_rate（学习率）</a>
                  <a class="train_par_content_ac">决定训练过程中权重调整的步长</a>
                </div>                
                <div id="weight_decay" class="train_par_content">
                  <a class="train_par_content_at">weight_decay（权重衰减）</a>
                  <a class="train_par_content_ac">一种正则化技术，防止机器学习模型过拟合，默认是0，初始可以设置为学习率的1/10，出现过拟合现象后可以逐步调大此参数</a>
                </div>                
                <div id="scheduler" class="train_par_content">
                  <a class="train_par_content_at">scheduler（调度器）</a>
                  <a class="train_par_content_ac">调整优化器的学习率</a>
                </div>                
                <div id="T_max" class="train_par_content">
                  <a class="train_par_content_at">T_max（达成最小学习率周期）</a>
                  <a class="train_par_content_ac">搭配“余弦 / Cosine”使用的参数，推荐等于你的epoch数量，学习率会在这个值的时候降到最低</a>
                </div>                
                <div id="T_0" class="train_par_content">
                  <a class="train_par_content_at">T_0（重启次数）</a>
                  <a class="train_par_content_ac">搭配“余弦重启 / CosineWarmRestarts”使用的参数，重置学习率的次数，可以帮助模型跳出局部最小值</a>
                </div>                
                <div id="num_warmup_steps" class="train_par_content">
                  <a class="train_par_content_at">num_warmup_steps（预热步数）</a>
                  <a class="train_par_content_ac">搭配“常量预热 / constant_warmup”使用的参数，在这些预热步骤中，学习率会从一个较低的值逐渐增加到初始设定的学习率</a>
                </div>                
                <div id="logger_freq" class="train_par_content">
                  <a class="train_par_content_at">logger_freq（日志记录频率）</a>
                  <a class="train_par_content_ac">训练过程中日志记录的频率，单位是step（步）</a>
                </div>                                
                <div id="log_dir" class="train_par_content">
                  <a class="train_par_content_at">log_dir（日志位置）</a>
                  <a class="train_par_content_ac">日志存储的路径</a>
                </div>                                
                <div id="log_dir" class="train_par_content">
                  <a class="train_par_content_at">log_name（日志名字）</a>
                  <a class="train_par_content_ac">日志存储的名字</a>
                </div>
              </div>
            </div>
          </div>
          <div class="triangle_box">
            <div class="triangle_box_one">
              <div class="triangleup" v-show="!showTriangleDown"></div>
              <div class="triangledown" v-show="showTriangleDown"></div>
            </div>
          </div>
          <div class="right-sidebar-downbox">
          </div>
      </div>
    </div>
  </div>
</template>
<script>
import ConfigForm from './ConfigForm.vue';
import ModelLocal from './ModelLocal.vue';
import ImageName from './ImageName.vue';
import PromptCreate from './PromptCreate.vue';
import axios from 'axios';

// eventBus.js
import mitt from 'mitt';
export const eventBus = mitt();

export default {
  name: 'App',
  components: {
    ConfigForm,
    ModelLocal,
    ImageName,  
    PromptCreate,
  },
  data() {
    return {
      // 添加一个新属性来控制哪个组件显示
      activeComponent: 'ConfigForm', // 默认显示 ImageName 组件
      hovered: '',
      showTriangleDown: true,
      lastScrollTop: 0, // 用于比较的上一次滚动位置
    }
  },
  methods: {
    setActiveComponent(componentName) {
      // 更新 activeComponent 的值，来切换显示的组件
      this.activeComponent = componentName;
    },
    handleSubmit(config) {
      axios.post('http://localhost:3000/update-config', config)
        .then(response => {
          console.log('Config updated', response);
          // 添加用户反馈
        })
        .catch(error => {
          console.error('Error updating config', error);
          // 处理错误情况
        });
    },
    updatePretrainedModelPath(newPath) {
      this.configFormRef.updateModelPath(newPath);
    },
    handleScroll(event) {
      const element = event.target;
      const currentScrollTop = element.scrollTop;
      // 检测滚动方向
      if (currentScrollTop > this.lastScrollTop) {
        // 向下滚动
        this.showTriangleDown = true;
      } else if (currentScrollTop < this.lastScrollTop) {
        // 向上滚动
        this.showTriangleDown = false;
      }

      // 更新上一次的滚动位置
      this.lastScrollTop = currentScrollTop;
    },
  },
};
</script>

<style>
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
  font-family: 'Segoe UI', Tahoma, Verdana, sans-serif;
}

body, html {
  background-color: #f7f7f7;
  margin: 0;
  padding: 0;
  height: 100%;
  box-sizing: border-box;
}

.container {
    display: flex;
    height: 100%;
    flex-direction: row; /* 子元素水平排列 */
    /* align-items: stretch; 子元素高度拉伸以填满容器高度 */
  }

/* 左侧边栏样式 */
.left-sidebar {
  display: flex; /* 启用 flex 布局 */
  flex-direction: column; /* 子元素垂直排列 */
  width: 240px;
  padding: 30px 20px 80px 30px;
  height: 100vh;
  position: fixed;
  left: 0;
  top: 0;
  overflow-y: auto;
}

.left-sidebar-block{
  display: flex; /* 启用 Flexbox 布局 */
  flex-direction: column; /* 子元素垂直排列 */
  width: 180px;
  padding: 20px 20px 40px 32px;
  color: #333; /* 深色文字 */
  height: 100vh;
  left: 0;
  top: 0;
  overflow-y: auto;
  border-radius: 20px; /* 圆角边框 */
  border-right: 3px solid #ffffff; /* 设置右边框为2像素宽的白色 */
  box-shadow: 12px 8px 20px #dadae764, 
    -8px -2px 18px #dedee8; /* 增强左上角阴影 */
  background: #ececec; /* Fallback color */
  background-image: linear-gradient(-145deg, #f4f4f4, #ebebed); 
}

.left-sidebar-box {
  flex-grow: 1; /* 允许该元素占据所有剩余空间 */
  overflow-y: auto; /* 如果内容超出，允许滚动 */
  margin-top: 30px; /* 与顶部的距离 */
}

.left-sidebar-box-option{
  display: flex; /* 启用Flexbox布局 */
  align-items: center; /* 垂直居中 */
  justify-content: flex-start; /* 水平方向从左边开始排列，你也可以根据需要改为center, space-between等 */
  position: relative; /* 相对定位 */
}

.left-sidebar ul {
  list-style-type: none;
}

.left-sidebar ul li {
  padding: 10px 0  ; /* 增加填充 */
  cursor: pointer;
  margin: 6px 0; /* 增加列表项之间的间距 */
  transition: all 0.2s ease; /* 平滑过渡效果 */
}

.note_dot {
  position: absolute;
  top: 50%;
  right: 10px;
  transform: translateY(-50%);
  width: 8px;
  height: 8px;
  background-color: rgb(206, 206, 206);
  border-radius: 50%;
  transition: opacity 0.3s;
  opacity: 0; /* 默认不显示 */
}

.left-sidebar-box-option:hover .note_dot,
.left-sidebar-box-option.active .note_dot {
  opacity: 1; /* 鼠标悬停或选项激活时显示 */
}

.left-sidebar-box-option.active .note_dot {
  background-color: rgb(4, 0, 255); /* 鼠标悬停或激活时的颜色 */
}

.note_dot_nothing{
  flex-grow: 1;
}

.sign-nothing {
  flex-shrink: 0; /* 防止缩小 */
  /* 可以添加更多样式，如背景颜色等 */
}

.sign-box{
  bottom: 20px; /* 距离底部0 */
  width: 100%; /* 让div宽度与视口宽度一样 */
  text-align: center; /* 文本居中显示 */
  padding: 10px 0; /* 填充 */
  border-radius: 20px;
  background-color: #ededed;
  box-shadow: 
  8px 8px 15px #c1c1c1, /* 外部阴影，右下方向 */
    -8px -8px 15px #ffffff, /* 外部高光，左上方向 */
    inset 5px 5px 10px #ffffff, /* 内部阴影，右下方向 */
    inset -4px -4px 10px #cecece; /* 内部高光，左上方向 */
  color: rgb(225, 225, 225);

}

.sign-box-link {
  text-decoration: none; /* 移除下划线 */
  color: rgb(16, 8, 255); /* 设置文字颜色为黑色 */
  font-weight: bold;
}

/* 主内容区域样式 */
.content {
  flex-grow: 1; /* 允许内容区域占用所有可用空间 */
  padding: 20px; /* 内边距 */
  margin-left: 220px; /* 与左侧边栏宽度相同 */
  margin-right: 380px; /* 与右侧边栏宽度相同 */
  flex-direction: column; /* 子元素垂直排列 */
  align-items: center; /* 子元素在交叉轴上（水平方向）居中 */
  justify-content: center; /* 子元素在主轴上（垂直方向）居中，如果你也想要垂直居中的话 */
}

/* 右侧边栏样式 */
.right-sidebar {
  width: 380px;
  border-left: 3px solid #ffffff;
  box-shadow: 12px 8px 26px #e4e4f064, 
    -8px -2px 18px #e2e2ee; /* 增强左上角阴影 */
  padding: 20px;
  color: #333;
  height: 100vh; /* Full height */
  position: fixed; /* 固定定位 */
  right: 0; /* 距离右侧0距离 */
  top: 0; /* 距离顶部0距离 */
  background-image: linear-gradient(145deg, #f4f4f4, #d9d9e0); 
}

.right-sidebar-up {
  height: 260px;
  display: flex; /* 启用 Flexbox 布局 */
  flex-direction: column; /* 子元素垂直排列 */
  align-items: flex-start; /* 子元素在水平轴上左对齐 */
  padding: 15px; /* 添加一些内边距 */
}

.right-sidebar-down{
  max-height: 700px;
  
  padding-right: 10px; /* 防止内容直接贴到边框 */
}

.right-box{
  display: flex; /* 启用 Flexbox 布局 */
  flex-direction: column; /* 子元素垂直排列 */
  height: 100%; /* 设置高度为 100%，以确保占满整个父容器 */
  margin: 40px 10px 20px 10px;
}

/* 针对Webkit浏览器如Safari和Chrome的滚动条隐藏 */
.right-sidebar-down::-webkit-scrollbar {
  display: none; /* 隐藏滚动条 */
}

.train_par_content_box::-webkit-scrollbar {
  display: none; /* 隐藏滚动条 */
}

/* 针对IE和Edge的滚动条隐藏 */
.right-sidebar-down {
  -ms-overflow-style: none;  /* IE和Edge */
  scrollbar-width: none;  /* Firefox */
}

.right-sidebar-up h2 {
  margin-bottom: 20px; /* 在标题和列表之间添加一些间距 */
}

.right-sidebar-downbox {
  flex-grow: 1; /* 允许此元素填充剩余空间 */
  /* 这里可以添加 right-sidebar-down 的样式 */
}

.train_line {
  display: block; /* 使a标签表现得像块级元素 */
  margin-bottom: 10px; /* 在每个训练步骤之间添加一些间距 */
  font-size: 14px; /* 设置合适的字体大小 */
  color: #333; /* 选择一个清晰易读的颜色 */
  text-decoration: none; /* 移除下划线 */
}

.train_par_content_title {
  margin-bottom: 20px; 
}

.train_par_content_box {
  overflow-y: auto;
}

.train_par_content_at ,.train_par_content_ac {
  display: block; /* 使a标签表现得像块级元素 */
  font-size: 14px; /* 设置合适的字体大小 */
  color: #333; /* 选择一个清晰易读的颜色 */
}

.train_par_content_at{
  margin-bottom: 8px; /* 在每个训练步骤之间添加一些间距 */
}

.train_par_content_ac{
  margin-bottom: 12px; /* 在每个训练步骤之间添加一些间距 */
}

.train_par_content {
  border-bottom: 1px solid #ccc; /* 添加灰色的底部边框 */
  padding-bottom: 10px; /* 底部填充，确保内容与边框之间有间隙 */
  margin-bottom: 15px; /* 底部外边距，确保相邻元素之间有空间 */
}

.triangle_box{
  display: flex;
  margin-top: 40px;
  width: auto;
  justify-content: center; /* 水平居中 */
}

.triangledown {
    width: 0;
    height: 0;
    border-left: 8px solid transparent;
    border-right: 8px solid transparent;
    border-top: 10px solid rgb(4, 0, 255); /* 蓝色三角形 */
    margin: 20px; /* 为了可视化，添加一些外边距 */
}

.triangleup{
    width: 0;
    height: 0;
    border-left: 8px solid transparent;
    border-right: 8px solid transparent;
    border-bottom: 10px solid rgb(4, 0, 255); /* 蓝色三角形 */
    margin: 20px; /* 为了可视化，添加一些外边距 */
}



/* 默认显示triangledown三角形 */
.triangledown {
    display: block;
}

/* 当左侧或右侧边栏被触发时，调整主内容区的边距 */
.active-left #app {
  margin-left: 200px; /* 为左侧边栏留出空间 */
}

.active-right #app {
  margin-right: 200px; /* 为右侧边栏留出空间 */
}

</style>

