const express = require('express');
const fs = require('fs');
const yaml = require('js-yaml');
const { spawn } = require('child_process');
const cors = require('cors');
const app = express();
const port = 3000;
const path = require('path');

// 使用 ws 库设置 WebSocket 服务器
const WebSocket = require('ws');
const wss = new WebSocket.Server({ noServer: true }); // noServer 选项表示我们将在 HTTP 服务器上处理 WebSocket 握手

// 假设您的虚拟环境位于项目根目录下的 'convenv' 文件夹中
const pythonExecutable = path.join(__dirname, '..', 'convenv', 'Scripts', 'python');
const conTrainYaml = path.join(__dirname, '..', 'par', 'controlnet_train.yaml');
const createConPath = path.join(__dirname, '..', 'par','createcon.yaml');
const imageNamePath = path.join(__dirname, '..', 'par','imagename.yaml');
const promptPath = path.join(__dirname, '..', 'par','promptcreate.yaml');

app.use(cors()); // 启用 CORS
app.use(express.json()); // 用于解析 JSON 格式的 body-parser 中间件

let trainingProcess = null; // 存储训练进程的引用

// 开始训练的端点 ConfigForm.vue
app.post('/start-training', (req, res) => {
  const configUpdates = req.body;

  try {
    // 读取现有的 YAML 文件
    let fileContents = fs.readFileSync(conTrainYaml, 'utf8');
    let config = yaml.load(fileContents);

    // 在写入 YAML 前确保 precision 是正确的数据类型
    if (typeof configUpdates.precision === 'string') {
      configUpdates.precision = configUpdates.precision === 'bf16' ? 'bf16' : parseInt(configUpdates.precision, 10);
    }

    // 根据 train_times 的值来决定是否使用 shuffle 或 sampleshuffle
    if (configUpdates.train_times > 1) {
      config.shuffle = false;
      config.sampleshuffle = configUpdates.sampleshuffle;
    } else {
      config.shuffle = configUpdates.shuffle; // 当 train_times 等于 1 时，我们使用 shuffle 参数
    }

    // 更新配置参数
    Object.assign(config, configUpdates);

    // 将更新后的对象转换回 YAML 格式并写回文件
    fs.writeFileSync(conTrainYaml, yaml.dump(configUpdates), 'utf8');

    const env = Object.assign(process.env, {
      NO_PROXY: 'huggingface.co', // 忽略代理的域名列表
      HTTP_PROXY: '', // 清空可能存在的代理设置
      HTTPS_PROXY: ''
    });

    // 运行训练脚本 `cwd` 设置为项目根目录
    const tutorialTrainScript = path.join(__dirname, '..', 'controlnet_sd15_train.py');
    trainingProcess = spawn(pythonExecutable, [tutorialTrainScript], { cwd: path.join(__dirname, '..'), env });

    trainingProcess.stdout.on('data', (data) => {
      console.log(`stdout: ${data}`);
    });

    trainingProcess.stderr.on('data', (data) => {
      console.error(`stderr: ${data}`);
    });

    trainingProcess.on('exit', (code) => {
      console.log(`Training process exited with code ${code}`);
      trainingProcess = null; // 清理引用
    });
           
    res.status(202).send({ message: '训练开始' });
  } catch (error) {
    console.error(error);
    res.status(500).send('更新配置或运行脚本时出错');
  }
  
});

// 停止训练的端点 ConfigForm.vue
app.post('/stop-training', (req, res) => {
  if (trainingProcess && !trainingProcess.killed) {
    trainingProcess.kill('SIGINT'); // 发送中断信号
    res.status(200).send({ message: '训练结束' });
  } else {
    res.status(400).send({ message: '没有发现正在训练的进程' });
  }
});

// 接收 modeldir.vue 传过来的模型路径并更新 createcon.yaml
app.post('/update-model-paths', (req, res) => {
  console.log('Request body:', req.body); // 确保后端正确接收了前端发送的数据
  const { inputModelPath, combinedOutputPath } = req.body;

  // 构建新的 YAML 内容
  const newYamlContent = {
    input_model_path: inputModelPath,
    combinedOutputPath: combinedOutputPath,
  };

  console.log('Received data:', newYamlContent);// 这将在服务器的控制台中显示 YAML 内容

  try {
    fs.writeFileSync(createConPath, yaml.dump(newYamlContent));
    console.log('YAML file updated successfully.');

    // 执行 Python 脚本
    const scriptPath = path.join(__dirname, '..', 'create_control.py');
    console.log(`Attempting to run script: ${scriptPath}`);

    const scriptProcess = spawn(pythonExecutable, [scriptPath]);

    res.send('模型路径已更新');
  } catch (error) {
    console.error('Error writing to YAML file:', error);
    res.status(500).send('更新 YAML 文件时发生错误');
  }
}); 

// 触发 tool_add_control.py (modeldir.vue)
app.post('/trigger-script', (req, res) => {
  const scriptPath = path.join(__dirname, '..', 'create_control.py');
  console.log(`Attempting to run script: ${scriptPath}`) // 打印
  const cwd = path.join(__dirname, '..'); // 设置 cwd（当前工作目录）为 tool_add_control.py 文件的目录
  // 注意：设置 cwd 为 'server.js' 所在的目录的父目录，即项目的根目录
  const scriptProcess = spawn(pythonExecutable, [scriptPath], { cwd });

  scriptProcess.stdout.on('data', (data) => {
    console.log(`stdout: ${data}`);
  });

  scriptProcess.stderr.on('data', (data) => {
    console.error(`stderr: ${data}`);
  });

  scriptProcess.on('close', (code) => {
    if (code === 0) {
      res.send('模型生成脚本已成功执行');
    } else {
      res.status(500).send(`模型生成脚本执行出错，退出码: ${code}`);
    }
  });
});

// 接收 ImageName.vue 传过来的模型路径并更新 ImageName.yaml
app.post('/update-image-yaml', (req, res) => {
  console.log('Request body:', req.body); // 确保后端正确接收了前端发送的数据
  const { imageDir } = req.body;

  // 构建新的 YAML 内容
  const newImageNameYaml = {
    imageDir: imageDir,
  };

  console.log('Received data:', newImageNameYaml);// 这将在服务器的控制台中显示 YAML 内容

  try {
    fs.writeFileSync(imageNamePath, yaml.dump(newImageNameYaml));
    console.log('YAML file updated successfully.');
    res.send('模型路径已更新');
  } catch (error) {
    console.error('Error writing to YAML file:', error);
    res.status(500).send('更新 YAML 文件时发生错误');
  }
}); 

// 触发 named.py (ImageName.vue )
app.post('/named-script', (req, res) => {
  const scriptPath = path.join(__dirname, '..', 'functionDir', 'named.py');
  console.log(`Attempting to run script: ${scriptPath}`) // 打印
  
  // 设置 cwd 为 server.js 文件的上级目录，即项目根目录
  const cwd = path.join(__dirname, '..');
  const scriptProcess = spawn(pythonExecutable, [scriptPath], { cwd });

  scriptProcess.stdout.on('data', (data) => {
    console.log(`stdout: ${data}`);
  });

  scriptProcess.stderr.on('data', (data) => {
    console.error(`stderr: ${data}`);
  });

  scriptProcess.on('close', (code) => {
    if (code === 0) {
      res.send('模型生成脚本已成功执行');
    } else {
      res.status(500).send(`模型生成脚本执行出错，退出码: ${code}`);
    }
  });
});

// 接收 PromptCreate.vue 传过来的模型路径并更新 promptcreate.yaml
app.post('/update-prompt-yaml', (req, res) => {
  console.log('Request body:', req.body); // 确保后端正确接收了前端发送的数据
  const { PromptCreate } = req.body;

  // 构建新的 YAML 内容
  const newPromptCreate = {
    PromptCreate: PromptCreate,
  };

  console.log('Received data:', newPromptCreate);// 这将在服务器的控制台中显示 YAML 内容

  try {
    fs.writeFileSync(promptPath, yaml.dump(newPromptCreate));
    console.log('YAML file updated successfully.');
    res.send('模型路径已更新');
  } catch (error) {
    console.error('Error writing to YAML file:', error);
    res.status(500).send('更新 YAML 文件时发生错误');
  }
}); 

// 触发 promptcreate.py (PromptCreate.vue )
app.post('/prompt-script', (req, res) => {
  const scriptPath = path.join(__dirname, '..', 'functionDir', 'promptcreate.py');
  console.log(`Attempting to run script: ${scriptPath}`) // 打印
  
  // 设置 cwd 为 server.js 文件的上级目录，即项目根目录
  const cwd = path.join(__dirname, '..');
  const scriptProcess = spawn(pythonExecutable, [scriptPath], { cwd });

  scriptProcess.stdout.on('data', (data) => {
    console.log(`stdout: ${data}`);
  });

  scriptProcess.stderr.on('data', (data) => {
    console.error(`stderr: ${data}`);
  });

  scriptProcess.on('close', (code) => {
    if (code === 0) {
      res.send('模型生成脚本已成功执行');
    } else {
      res.status(500).send(`模型生成脚本执行出错，退出码: ${code}`);
    }
  });
});


app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});

