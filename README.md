# AI Grandson Chatbot

## 项目简介

AI Grandson Chatbot 是一个使用 AI 技术开发的聊天机器人，旨在模拟孙子与爷爷的对话。通过自然语言处理和高质量的文本转语音转换，这个项目能够为孤独的老年人提供温暖和陪伴。该系统具备以下功能：

1. **模拟孙子角色的对话**：通过 AI 模拟一个16岁以下的孩子，与老年人进行互动，提供温暖和陪伴。
2. **高质量文本转语音**：使用阿里云的语音合成服务，将生成的文本转换成语音并播放。
3. **中英文翻译**：将中文输入翻译成英文，通过 AI 生成英文回复，再将回复翻译回中文。

## 功能描述

### 1. 模拟孙子角色的对话

使用 OpenAI 的语言模型，设计一个孙子角色，具备以下特质：
- 聪明
- 善良
- 孝顺
- 活泼
- 开朗

通过对话历史和输入，生成充满童真和感情的回应。

### 2. 高质量文本转语音

使用阿里云的语音合成服务，将 AI 生成的回复转换为高质量的语音文件并播放，使对话更加生动和真实。

### 3. 中英文翻译

利用阿里云翻译服务，将中文输入翻译成英文，再将 AI 生成的英文回复翻译回中文，确保对话的流畅性和自然性。

## 代码说明

### 环境配置

在运行该程序前，需要确保安装以下依赖：

- `langchain`
- `dotenv`
- `playsound`
- `dashscope`
- `alibabacloud_alimt20181012`
- `alibabacloud_tea_openapi`
- `alibabacloud_tea_util`
- `flask`

请使用以下命令安装依赖：

```bash
pip install langchain python-dotenv playsound dashscope alibabacloud_alimt20181012 alibabacloud_tea_openapi alibabacloud_tea_util flask
