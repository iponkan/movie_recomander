import os
import shutil
import re

def safe_rename(old_path, new_path):
    """ 安全地进行大小写重命名，解决 Windows 系统的冲突 """
    if not os.path.exists(old_path):
        return
    
    # 获取磁盘上真实的大小写名称
    parent = os.path.dirname(old_path) or "."
    base = os.path.basename(old_path)
    actual_name = next((f for f in os.listdir(parent) if f.lower() == base.lower()), None)
    
    if not actual_name:
        return
    
    target_name = os.path.basename(new_path)
    
    # 如果已经是完全匹配的小写，则跳过
    if actual_name == target_name:
        return
        
    # Windows 无法直接把 A 重命名为 a，必须通过中转名称
    temp_path = old_path + "_temp_rename"
    if os.path.exists(temp_path):
        shutil.rmtree(temp_path) if os.path.isdir(temp_path) else os.remove(temp_path)
        
    os.rename(os.path.join(parent, actual_name), temp_path)
    os.rename(temp_path, new_path)
    print(f"✅ 成功规范化: {actual_name} -> {target_name}")

def comprehensive_refactor():
    print("🚀 开始深度重构项目结构 (V3 强力版)...")

    # 1. 重命名顶级目录
    top_dirs = ["Algorithms", "Datasets", "Instance", "Website_Results"]
    for d in top_dirs:
        safe_rename(d, d.lower())

    # 2. 规范化 Frontend 目录及其子项
    if os.path.exists("Frontend"):
        # 模板处理
        if os.path.exists("Frontend/Templates"):
            if os.path.exists("templates"): shutil.rmtree("templates")
            shutil.move("Frontend/Templates", "templates")
            print("✅ 移动模板: Frontend/Templates -> templates")
        
        # 静态资源处理
        if os.path.exists("Frontend/Static"):
            if os.path.exists("static"): shutil.rmtree("static")
            shutil.move("Frontend/Static", "static")
            print("✅ 移动静态资源: Frontend/Static -> static")
            
        try: shutil.rmtree("Frontend")
        except: pass

    # 3. 治理 static 内部的混乱命名 (Css, Images, JS Files)
    if os.path.exists("static"):
        # 修复子目录大小写
        safe_rename("static/Css", "static/css")
        safe_rename("static/Images", "static/images")
        # 特别修复带空格的 JS Files
        if os.path.exists("static/JS Files"):
            safe_rename("static/JS Files", "static/js")

    # 4. 批量更新代码和 HTML 引用
    for py_f in ["app.py", "original_lightgcn.py"]:
        if os.path.exists(py_f):
            with open(py_f, 'r', encoding='utf-8') as f:
                content = f.read()
            content = content.replace("Datasets/", "datasets/").replace("Frontend/Templates", "templates")
            content = content.replace("Frontend/Static", "static").replace("'/Static'", "'/static'")
            content = re.sub(r"Flask\(__name__.*?\)", "Flask(__name__)", content)
            with open(py_f, 'w', encoding='utf-8') as f:
                f.write(content)

    if os.path.exists("templates"):
        for root, _, files in os.walk("templates"):
            for file in files:
                if file.endswith(".html"):
                    p = os.path.join(root, file)
                    with open(p, 'r', encoding='utf-8') as f:
                        h = f.read()
                    h = h.replace("/Static/JS Files/", "/static/js/").replace("/Static/Css/", "/static/css/")
                    h = h.replace("/Static/Images/", "/static/images/").replace("/Static/", "/static/")
                    with open(p, 'w', encoding='utf-8') as f:
                        f.write(h)
                    print(f"🎨 HTML 已更新: {file}")

    print("\n✨ 重构圆满完成！")

if __name__ == "__main__":
    comprehensive_refactor()