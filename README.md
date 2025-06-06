# Note - WeChat AI Assistant

本项目实现一个简易的微信 "随手记" 助手，自动将微信消息同步到飞书文档，主要功能如下：

1. 监听个人或群聊消息（文字、链接、图片）。
2. 根据内容自动分类：
   - 链接信息置顶保存；
   - 自动识别待办事项（如包含 "TODO"、"待办"、"记得" 等关键词）；
   - 自动识别灵感内容（如包含 "灵感"、"idea"、"想法" 等关键词）；
3. 图片会上传到飞书云盘并在文档中以链接形式展示。
4. 默认每天生成一份飞书文档，也可改为持续更新同一文档。
5. 所有操作在后台自动完成。

## 部署与运行

```bash
./deploy.sh
```

首次运行会要求微信扫码登录。

## 需要申请的飞书 API 权限

- `auth:tenant` 获取租户级访问 token
- `doc:doc` 新建及编辑文档
- `drive:file` 上传文件到云盘

请在飞书开放平台创建应用并配置以上权限范围，获取 `app_id` 和 `app_secret` 填写到 `src/config.py` 中。
