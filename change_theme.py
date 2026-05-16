import re

with open("C:/Users/Administrator.DESKTOP-K1RSGDC/WorkBuddy/520aj/index.html", "r", encoding="utf-8") as f:
    content = f.read()

# 1. 改标题
content = content.replace("<title>SHOES GALLERY</title>", "<title>520AJ 球鞋展示</title>")

# 2. 改页面大标题（Logo文字）
content = content.replace('<div class="logo">SHOES GALLERY</div>', '<div class="logo">520AJ</div>')

# 3. 改 body 背景和文字颜色（深色 -> 浅色）
content = content.replace("background: #0a0a0a;  /* 深黑色背景 */", "background: #f5f5f5;  /* 浅灰背景 */")
content = content.replace("color: #fff;         /* 白色文字 */", "color: #111;         /* 深色文字 */")

# 4. 改导航栏背景（深色半透明 -> 浅色半透明）
content = content.replace(
    "background: rgba(10, 10, 10, 0.95); /* 半透明黑色背景 */",
    "background: rgba(255, 255, 255, 0.95); /* 半透明白色背景 */"
)
content = content.replace(
    "border-bottom: 1px solid rgba(255, 255, 255, 0.1); /* 底部细线 */",
    "border-bottom: 1px solid rgba(0, 0, 0, 0.08); /* 底部细线 */"
)

# 5. Logo 渐变色（白色渐变 -> 红色渐变，呼应 520 主题）
content = content.replace(
    "background: linear-gradient(135deg, #fff 0%, #888 100%);",
    "background: linear-gradient(135deg, #e74c3c 0%, #ff6b6b 100%);"
)

# 6. 导航按钮样式（深色 -> 浅色带红色边框）
content = content.replace(
    """    .nav-btn {
      background: rgba(255,255,255,0.1); /* 半透明背景 */
      border: 1px solid rgba(255,255,255,0.2); /* 半透明白色边框 */
      color: #fff;                      /* 白色文字 */
      padding: 8px 18px;
      border-radius: 20px;               /* 圆角胶囊形 */
      cursor: pointer;
      font-size: 14px;
      transition: all 0.3s ease;        /* 平滑过渡动画 */
    }""",
    """    .nav-btn {
      background: #fff;
      border: 1px solid #e74c3c;
      color: #e74c3c;
      padding: 8px 18px;
      border-radius: 20px;
      cursor: pointer;
      font-size: 14px;
      transition: all 0.3s ease;
    }"""
)

# 7. 导航按钮 hover
content = content.replace(
    """    .nav-btn:hover {
      background: rgba(255,255,255,0.25);
      border-color: rgba(255,255,255,0.4);
      transform: translateY(-1px);      /* 微微上移效果 */
    }""",
    """    .nav-btn:hover {
      background: #e74c3c;
      color: #fff;
      transform: translateY(-1px);
    }"""
)

# 8. 导航按钮激活状态
content = content.replace(
    """    .nav-btn.active {
      background: #fff;
      color: #111;
      border-color: #fff;
      font-weight: 600;
    }""",
    """    .nav-btn.active {
      background: #e74c3c;
      color: #fff;
      border-color: #e74c3c;
      font-weight: 600;
    }"""
)

# 9. 搜索框（深色 -> 浅色）
content = content.replace(
    """    .search-box {
      flex: 1;               /* 占据剩余空间 */
      max-width: 400px;       /* 最大宽度 */
      position: relative;
    }

    /* 搜索输入框 */
    .search-box input {
      width: 100%;
      padding: 10px 40px 10px 16px;  /* 右侧留空间给搜索图标 */
      border-radius: 20px;             /* 圆角 */
      border: 1px solid rgba(255,255,255,0.2);
      background: rgba(255,255,255,0.1);
      color: #fff;
      font-size: 14px;
      outline: none;                   /* 去掉点击时的默认边框 */
      transition: all 0.3s ease;
    }

    /* 输入框聚焦状态 */
    .search-box input:focus {
      border-color: rgba(255,255,255,0.5);
      background: rgba(255,255,255,0.15);
      box-shadow: 0 0 20px rgba(255,255,255,0.1);
    }

    /* 输入框提示文字颜色 */
    .search-box input::placeholder {
      color: rgba(255,255,255,0.4);
    }""",
    """    .search-box {
      flex: 1;
      max-width: 400px;
      position: relative;
    }

    .search-box input {
      width: 100%;
      padding: 10px 40px 10px 16px;
      border-radius: 20px;
      border: 1px solid #ddd;
      background: #fff;
      color: #111;
      font-size: 14px;
      outline: none;
      transition: all 0.3s ease;
    }

    .search-box input:focus {
      border-color: #e74c3c;
      background: #fff;
      box-shadow: 0 0 20px rgba(231,76,60,0.1);
    }

    .search-box input::placeholder {
      color: #999;
    }"""
)

# 10. 搜索图标颜色
content = content.replace("color: rgba(255,255,255,0.5);", "color: #999;")
content = content.replace(
    """      color: rgba(255,255,255,0.5);
      transition: color 0.3s ease;""",
    """      color: #999;
      transition: color 0.3s ease;"""
)

with open("C:/Users/Administrator.DESKTOP-K1RSGDC/WorkBuddy/520aj/index.html", "w", encoding="utf-8") as f:
    f.write(content)

print("主题色替换完成！")
