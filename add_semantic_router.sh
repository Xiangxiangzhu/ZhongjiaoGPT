#!/bin/bash

# 设置脚本在遇到错误时停止执行
set -e

# Git仓库URL
repoURL="https://github.com/Xiangxiangzhu/semantic-router.git"

# 要克隆的分支名称
branchName="local-emb"

# 克隆特定分支
echo "Cloning the repository from $repoURL..."
git clone -b $branchName --single-branch $repoURL

# 检查目录是否存在
if [ ! -d "semantic-router" ]; then
    echo "Failed to clone repository."
    exit 1
fi

# 创建目标目录
echo "Creating target directory..."
mkdir -p modules/models

# 移动semantic_router目录到指定位置
echo "Moving directories..."
mv semantic-router/semantic_router modules/models

# 清理（可选）
echo "Cleaning up..."
rm -rf semantic-router

echo "Script completed."
