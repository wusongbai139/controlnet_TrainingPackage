<template>
  <div class="config-form-body">
    <div class="config-form">
      <h2 class="config_title">controlnet_SD15 训练器</h2>
      <form @submit.prevent="startTraining">
        <div class="prabox">
            <div class="praen">pretrained_model_path</div>
            <div class="pracn">
                <label for="pretrained_model_path">预训练模型位置</label>
            </div>
            <input class="input_box" id="pretrained_model_path" v-model="config.pretrained_model_path" type="text">
        </div>
        <div class="prabox">
            <div class="praen">training_set_path</div>
            <div class="pracn">
                <label for="Datadir" class="pracn">训练集文件夹</label>
            </div>
            <input class="input_box" id="Datadir" v-model="config.Datadir" type="text">
        </div>
        <div class="prabox">
            <div class="praen">model_name</div>
            <div class="pracn">
                <label for="ModelName" class="pracn">新模型名称</label>
            </div>
            <input class="input_box" id="ModelName" v-model="config.ModelName" type="text">
        </div>
        <div class="prabox">
            <div class="praen">SD_Locked</div>
            <div class="pracn">
                <label for="sd_locked" class="pracn">SD锁定</label>
            </div>
            <input class="input_box checkboxin" type="checkbox" id="sd_locked" v-model="config.sd_locked">
        </div>
        <div class="prabox">
            <div class="praen">only_mid_control</div>
            <div class="pracn">
                <label for="only_mid_control" class="pracn">仅训练中间层</label>
            </div>
            <input class="input_box checkboxin" type="checkbox" id="only_mid_control" v-model="config.only_mid_control">
        </div>
        <div class="prabox">
            <div class="praen">precision</div>
            <div class="pracn">
                <label for="precision" class="pracn">训练精度</label>
            </div>
            <select class="input_box select_box" id="precision" v-model.number="config.precision">
                <option value="16">fp16</option>
                <option value="bf16">bf16</option>
                <option value="32">32</option>
            </select>
        </div>
        <div class="prabox">
            <div class="praen">batch_size</div>
            <div class="pracn">
                <label for="batch_size" class="pracn">并行训练数量</label>
            </div>
            <input class="input_box" id="batch_size" v-model="config.batch_size" type="number" min="1" step="1">
        </div>
        <div class="prabox">
            <div class="praen">accumulate_grad_batches</div>
            <div class="pracn">
                <label for="accumulate_grad_batches" class="pracn">累计梯度批次</label>
            </div>
            <input class="input_box" id="accumulate_grad_batches" v-model="config.accumulate_grad_batches" type="number">
        </div>
        <div class="prabox">
            <div class="praen">num_workers</div>
            <div class="pracn">
                <label for="num_workers" class="pracn">并行处理进程（建议默认0）</label>
            </div>
            <input class="input_box" id="num_workers" v-model="config.num_workers" type="number" min="0" oninput="validity.valid||(value='');">
        </div>
        <div class="prabox">
            <div class="praen">max_epochs</div>
            <div class="pracn">    
                <label for="max_epochs" class="pracn">最大训练轮数</label>
            </div>
            <input class="input_box" id="max_epochs" v-model="config.max_epochs" type="number">
        </div>
        <div class="prabox">
            <div class="praen">repeats</div>
            <div class="pracn">
                <label for="train_times" class="pracn">每轮中数据重复训练次数</label>
            </div>
            <input class="input_box checkboxin" type="number" id="train_times" v-model="config.train_times">
        </div>
        <div class="prabox">
            <div class="praen">shuffle</div>
            <div class="pracn">
                <label for="shuffle" class="pracn">随机数据集顺序</label>
            </div>
            <input class="input_box checkboxin" type="checkbox" id="shuffle" v-model="config.shuffle">
        </div>
        <div class="prabox">
            <div class="praen">save_every_n_epochs</div>
            <div class="pracn">
                <label for="every_n_epochs" class="pracn">每几轮保存一次</label>
            </div>
            <input class="input_box" id="every_n_epochs" v-model="config.every_n_epochs" type="number">
        </div>
        <div class="prabox">
            <div class="praen" style="color: rgb(16, 8, 255);font-weight: bold;">model_save_path</div>
            <div class="pracn">
                <label for="model_dir" class="pracn" style="color: rgb(16, 8, 255);font-weight: bold;">模型保存路径</label>
            </div>
            <input class="input_box" id="model_dir" v-model="config.model_dir" type="text">
        </div>
        <div class="prabox">
            <div class="praen">optimizer</div>
            <div class="pracn">
                <label for="optimizer" class="pracn">优化器</label>
            </div>
            <select class="input_box select_box" id="optimizer" v-model="config.optimizer">
                <option value="Adam">Adam</option>
                <option value="AdamW">AdamW</option>
                <option value="Lion">Lion</option>
                <option value="Prodigy">Prodigy</option>
            </select>
            <!-- 选择Prodigy，出现可选择参数 d_coef -->
            <div class="" v-if="config.optimizer === 'Prodigy'">
                <div class="praen">d_coef</div>
                <div class="pracn">
                    <label for="d_coef" class="pracn">学习率估计系数</label>
                </div>
                <input class="input_box" id="d_coef" v-model="config.d_coef" type="number" min="0">
            </div>
            <div class="" v-if="config.optimizer === 'Prodigy'">
                <div class="praen">safeguard_warmup</div>
                <div class="pracn">
                    <label for="safeguard_warmup " class="pracn swarm_safe">预热防护</label>
                </div>
                <input class="input_box checkboxin" id="safeguard_warmup " v-model="config.safeguard_warmup " type="checkbox">
            </div>
        </div>
        <div class="prabox"> 
            <div>通用设置</div>
            <div class="praboxlr">
                <div class="pralr">
                    <div class="praen"> - general_lr</div>
                    <div class="pracn">
                        <label for="general_lr" class="pracn"> - 通用学习率</label>
                    </div>
                    <input class="input_box" id="general_lr" v-model="config.general_lr" type="text">
                </div>
                <div class="pralr">
                    <div class="praen"> - general_weight_decay</div>
                    <div class="pracn">
                        <label for="general_wd" class="pracn"> - 通用权重衰减</label>
                    </div>
                    <input class="input_box" id="general_wd" v-model="config.general_wd" type="text">
                </div>
            </div>
        </div>
        <div class="prabox"> 
            <div>Unet设置</div>
            <div class="praboxlr">
                <div class="pralr">
                    <div class="praen"> - unet_lr</div>
                    <div class="pracn">
                        <label for="unet_lr" class="pracn"> - unet学习率</label>
                    </div>
                    <input class="input_box" id="unet_lr" v-model="config.unet_lr" type="text">
                </div>
                <div class="pralr">
                    <div class="praen"> - unet_weight_decay</div>
                    <div class="pracn">
                        <label for="unet_wd" class="pracn"> - unet权重衰减</label>
                    </div>
                    <input class="input_box" id="unet_wd" v-model="config.unet_wd" type="text">
                </div>
            </div>
        </div>
        <div class="prabox"> 
            <div>文本编码设置</div>
                <div class="praboxlr">
                    <div class="pralr">
                        <div class="praen"> - text_encoder_lr</div>
                        <div class="pracn">
                            <label for="text_encoder_lr" class="pracn"> - 文本编码学习率</label>
                        </div>
                        <input class="input_box" id="text_encoder_lr" v-model="config.text_encoder_lr" type="text">
                    </div>
                    <div class="pralr">
                        <div class="praen"> - text_encoder_weight_decay</div>
                        <div class="pracn">
                            <label for="text_encoder_wd" class="pracn"> - 文本编码权重衰减</label>
                        </div>
                        <input class="input_box" id="text_encoder_wd" v-model="config.text_encoder_wd" type="text">
                    </div>
                </div>
        </div>
        <div class="prabox">
            <div class="praen">scheduler</div>
            <div class="pracn">
                <label for="scheduler" class="pracn">调度器</label>
            </div>
            <select class="input_box select_box" id="scheduler" v-model="config.scheduler">
                <option value="CosineAnnealingLR">余弦 / Cosine</option>
                <option value="CosineAnnealingWarmRestarts">余弦重启 / CosineWarmRestarts</option>
                <option value="constant_warmup">常量预热 / constant_warmup</option>
            </select>
        
        <!-- 根据选择的调度器显示 T_max 输入字段 -->
        <div class="prabox" v-if="config.scheduler === 'CosineAnnealingLR'">
            <div class="praen">T_max</div>
            <div class="pracn">
                <label for="T_max" class="pracn">达成最小学习率周期</label>
            </div>
            <input class="input_box" id="T_max" v-model="config.T_max" type="number" min="0">
        </div>
        <!-- 根据选择的调度器显示 T_0 输入字段 -->
        <div class="prabox" v-if="config.scheduler === 'CosineAnnealingWarmRestarts'">
            <div class="praen">T_0</div>
            <div class="pracn">
                <label for="T_0" class="pracn">重启次数</label>
            </div>
            <input class="input_box" id="T_0" v-model="config.T_0" type="number" min="0">
        </div>
        <!-- 根据选择的调度器显示 T_0 输入字段 -->
        <div class="prabox" v-if="config.scheduler === 'constant_warmup'">
            <div class="praen">num_warmup_steps</div>
            <div class="pracn">
                <label for="num_warmup_steps" class="pracn">预热步数</label>
            </div>
            <input class="input_box" id="num_warmup_steps" v-model="config.num_warmup_steps" type="number" min="0">
        </div>
        </div>

        <div class="prabox">
            <div class="praen">logger_freq</div>
            <div class="pracn">
                <label for="logger_freq" class="pracn">日志记录频率</label>
            </div>
            <input class="input_box" id="logger_freq" v-model="config.logger_freq" type="number">
        </div>
        <div class="prabox">
            <div class="praen">log_dir</div>
            <div class="pracn">
                <label for="log_dir" class="pracn">日志位置</label>
            </div>
            <input class="input_box" id="log_dir" v-model="config.log_dir" type="text">
        </div>
        <div class="prabox">
            <div class="praen">log_name</div>
            <div class="pracn">
                <label for="log_name" class="pracn">日志名字</label>
            </div>
            <input class="input_box" id="log_name" v-model="config.log_name" type="text">
        </div>
        <div class="button-container">
          <button class="button-in" type="submit">开始训练</button>
          <button class="button-in" type="button" @click="stopTraining">停止训练</button>
        </div>
      </form>
    </div>
  </div>
</template>

<style scoped>

.config-form-body{
  width: auto;
  display: flex; /* 使用flexbox布局 */
  flex-direction: column; /* 子元素垂直排列 */
  align-items: center; /* 子元素在交叉轴上（水平方向）居中 */
  justify-content: center; /* 子元素在主轴上（垂直方向）居中，如果你也想要垂直居中的话 */
}

.config-form {
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

  /* 下拉菜单的 Neumorphism 风格样式 */
.select_box {
  background-color: #ffffff; /* 浅灰色背景 */
  border-radius: 12px; /* 圆角 */
  border: none; /* 无边框 */
  box-shadow: 
    8px 8px 16px #d1d1d1, /* 浅色阴影 */
    -8px -8px 16px #ffffff; /* 深色阴影 */
  padding: 10px 15px; /* 内部填充 */
  margin: 5px 0 15px 0; /* 外部间距 */
  font-size: 16px; /* 字体大小 */
  color: #333; /* 文本颜色 */
}

/* 当下拉菜单处于焦点时的样式 */
.select_box:focus {
  outline: none; /* 移除默认轮廓 */
  box-shadow: 
    0 0 0 2px rgba(0, 123, 255, 0.25), /* 蓝色边框高亮 */
    8px 8px 16px #d1d1d1, 
    -8px -8px 16px #ffffff;
}

/* 下拉菜单的选项样式 */
.select_box option {
  background-color: white; /* 选项的背景色 */
  color: #333; /* 选项的文本颜色 */
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

  .praboxlr {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    align-items: flex-start;
    gap: 20px;
  }

  .pralr {
    flex: 1 1 calc(50% - 10px);
    display: flex;
    flex-direction: column;
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
    background-image: linear-gradient(to left, #636bff, #4e54c8);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
    border-color: #8f94fb;
  }

  .button-in:active {
    transform: translateY(1px);
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
  }

  .checkboxin[type="checkbox"] {
    position: relative;
    width: 24px;
    height: 24px;
    -webkit-appearance: none;
    appearance: none;
    background: #eee;
    border-radius: 4px;
    border: 2px solid #ccc;
    cursor: pointer;
    transition: all 0.3s ease;
  }

  .checkboxin[type="checkbox"]:checked {
    background: #1e00ff;
    border-color: #409cff;
  }

  .checkboxin[type="checkbox"]:checked::after {
    content: '';
    position: absolute;
    top: 1px; left: 6px;
    width: 6px;
    height: 12px;
    border: solid white;
    border-width: 0 2px 2px 0;
    transform: rotate(45deg);
  }



</style>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      config: {
        pretrained_model_path: '',
        Datadir: '',
        ModelName: 'controlnet_sd15',
        batch_size: 1,
        every_n_epochs: 4,
        model_dir: '',
        max_epochs: 20,
        accumulate_grad_batches: 4,
        num_workers: '0',
        precision: '16',
        train_times: 1,
        shuffle: false,  // 默认值
        sampleshuffle: false,  // 这将根据 train_times 的值来动态更新
        optimizer: 'Adam', // 默认值
        safeguard_warmup: false,
        decouple: true,
        general_lr: '0.00005',
        general_wd: '0',
        unet_lr: '0.00005',
        unet_wd: '0',
        text_encoder_lr: '0.00005',
        text_encoder_wd: '0',
        scheduler: 'CosineAnnealingLR',
        T_max: 1,
        T_0: 2,
        sd_locked: true,
        only_mid_control: false,
        num_warmup_steps: 10 ,
        logger_freq: 300,
        log_dir: 'H:\\AIGC\\log',
        log_name: '1111',
      },
      trainingProcess: null,
    };
  },
  watch: {
    // 监听 train_times 的变化
    'config.train_times': function(newVal) {
      if (newVal > 1) {
        // 当 train_times 大于1时，设置 sampleshuffle 并禁用 shuffle
        this.config.shuffle = false;
        this.config.sampleshuffle = true;  // 或者基于一些其他的逻辑来设置这个值
      } else {
        // 当 train_times 等于1时，启用 shuffle
        this.config.shuffle = true;
        this.config.sampleshuffle = false;  // 确保 sampleshuffle 被禁用
      }
    }
  },
  methods: {
    startTraining() {
      // 发送请求到后端开始训练
      axios.post('http://localhost:3000/start-training', this.config)
        .then(response => {
          console.log('Training started', response);
          this.trainingProcess = response.data.process;
        })
        .catch(error => {
          console.error('Error starting training', error);
        });
    },
    stopTraining() {
      // 发送请求到后端停止训练
      axios.post('http://localhost:3000/stop-training', { process: this.trainingProcess })
        .then(response => {
          console.log('Training stopped', response);
        })
        .catch(error => {
          console.error('Error stopping training', error);
        });
    },
  },
 
};
</script>