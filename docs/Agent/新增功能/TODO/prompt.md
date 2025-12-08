写一个自动化python脚本测试刚才写的代码，注意登录发送的形式[登录接口使用的是 OAuth2PasswordRequestForm,需要用 form data 而不是 JSON!]，账号：Drew 密码：932087585@qq.com 写完 pytest 自行进行测试（OAuth2 form data，写到 backend\tests\ 目录下）中文显示有编码问题，不能使用 emoji 文字，但功能正常，所以不能出现乱码问题，将输出中的特殊字符改为ASCII

再次 Review并更新你刚才开发的所有代码，是否把要开发的所有要素都考虑到了？深度探索项目，是否符合预期,验证是否引入新问题,检查是否真正解决原问题,检查修改完整性,验证逻辑一致性,更深入的验证，确认问题是否真实存在，以及是否有遗漏的问题



cd D:\Java\ai_writer\backend
.\venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000



cd D:\Java\ai_writer
npm install
npm run dev





来确认细节：
  1.问题1: 左侧导航项的显示范围：选项A：仅在编辑器页面显示；
  2.问题2: 左侧导航项的分组位置：方案A：放在"创作"分组下；
  3.问题3: 点击行为和高亮状态：场景1：点击左侧"世界观"如果右侧未打开 → 打开世界观面板；如果右侧已经打开了"世界观"面板
  →保持打开；如果右侧打开的是其他面板（概括/AI） → 切换到世界观面板；
  场景2：高亮状态：当右侧世界观面板打开时 → 左侧"世界观"导航项高亮（蓝色背景）
  4.问题4: 状态管理方式：方案A：扩展现有的 editorStore；
  5.问题5: 图标选择：保持现在UI的风格。





1. 将 warning 中的 borderRadius 改为标准 border-radius 并按需做代码分块以降低 chunk 体积。
  2. 若想恢复强类型保护，可逐步移除 @ts-nocheck 并按模块补全类型与 API。

  帮我将代码提交到远程仓库的dev分支上，注释："feat:增加'@指令系统'，实现其中的引入知识库文档功能以及实现'@指令系统'浮层UI"