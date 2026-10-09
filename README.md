# Resident-Evil
DSBA Python group project
## 上手步骤（第一次使用）

1. **安装工具**：Python 3.10 以上、VS Code（装微软官方 Python 扩展）、Git（终端输入 `git --version` 检查）
2. **接受邀请**：在邮箱里接受 GitHub 仓库的协作者邀请
3. **下载仓库**：在 VS Code 按 `Ctrl+Shift+P`（Mac 用 `Cmd+Shift+P`），输入 `Git: Clone`，粘贴仓库的 HTTPS 地址，选一个本地文件夹，然后点"打开"
4. **创建虚拟环境**：在 VS Code 终端（`` Ctrl+` ``）运行：
python -m venv .venv
Mac/Linux 激活：`source .venv/bin/activate`
   激活成功后，终端最左边会出现 `(.venv)`
5. **安装依赖**：pip install -r requirements.txt
6. **选择解释器**：`Ctrl+Shift+P`（Mac 用 `Cmd+Shift+P`）→ `Python: Select Interpreter` → 选 `.venv` 里的那个
7. **验证**：运行 `python main.py`，看到 `project skeleton ready` 就成功了
8. **第一个任务**：在 `render.py` 里实现 `plot_sir(S, I, R)`，用 matplotlib 画出三条曲线（S、I、R）。写完后提交并推送：

git add render.py
git commit -m “add plot_sir”
git push


**每天开始工作前先运行 `git pull`，结束时 `git add`、`git commit`、`git push`。**

## 接口约定

| 项目 | 约定 |
|------|------|
| 状态表示 | 字符串 'S'、'I'、'R' |
| SIR 函数 | `simulate_sir(n, i0, beta, gamma, days)` 返回三个列表 `(S, I, R)`，每天一个值 |
| 画图函数 | `plot_sir(S, I, R)` 接收这三个列表并画图 |
| 参数来源 | 统一从 `config.py` 读取 |
| 文件分工 | `model.py` 只放计算，不画图；`render.py` 只放画图，不做计算 |