#!/bin/bash

# 进入 submodule 目录
cd modules/models || { echo "Submodule directory not found"; exit 1; }

# 拉取最新的变化
git pull origin dev || { echo "Failed to pull latest changes in submodule"; exit 1; }

# 返回主项目目录
cd ../.. || { echo "Failed to return to main project directory"; exit 1; }

# 更新 submodule 的引用
git add modules/models || { echo "Failed to add submodule"; exit 1; }

# 提交更改
git commit -m "Update submodule to latest commit" || { echo "Failed to commit changes"; exit 1; }

## 推送主项目的更改
#git push origin main || { echo "Failed to push changes to remote"; exit 1; }

echo "Submodule changes synced successfully!"
