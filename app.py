# app.py
from flask import Flask, request, render_template, redirect, url_for
import uuid
from typing import Dict, Any, List, Tuple

# 导入您刚刚完成的标签化逻辑函数
from mapping import get_element_ids

# =========================================================================
# 1. 初始化设置
# =========================================================================
app = Flask(__name__)

# 存储临时会话数据: UUID 对应计算出的所有结果 (ID列表和文本数据)
# 这是一个在内存中运行的字典，用于演示目的。
SESSION_DATA: Dict[str, Dict[str, Any]] = {}


# =========================================================================
# 2. 根路由：指标输入界面
# =========================================================================
@app.route('/', methods=['GET'])
def input_page():
    return render_template('input.html')


# =========================================================================
# 3. 提交路由：处理数据、运行逻辑、存储结果
# =========================================================================
@app.route('/submit', methods=['POST'])
def submit_indicators():
    """
    接收用户提交的表单数据，运行 mapping.py 逻辑，并存储结果。
    """
    
    # 1. 从表单中安全地获取数据，并进行类型转换
    try:
        # 获取数字指标 (并确保转换为整数)
        salary_expect = int(request.form.get('salary_expect', 0))
        age = int(request.form.get('age', 0))
        
        # 获取字符串指标
        nationality = request.form.get('nationality', '')
        mbti_type = request.form.get('mbti_type', '')
        bachelor_uni = request.form.get('bachelor_uni', '')
        master_uni = request.form.get('master_uni', '')
        major = request.form.get('major', '')

    except ValueError:
        # 如果年薪或年龄不是有效数字，返回错误提示
        return "error 404", 400

    # 2. 调用 mapping.py 中的逻辑函数
    # 接收两个返回值: 1. SVG ID 列表, 2. 文本数据字典
    selected_ids, raw_data = get_element_ids(
        salary_expect, nationality, mbti_type, bachelor_uni, master_uni, age, major
    )
    
    # 3. 创建唯一的会话 ID (UUID)
    session_id = str(uuid.uuid4())
    
    # 4. 存储所有结果数据到内存中
    SESSION_DATA[session_id] = {
        'element_ids': selected_ids, # SVG/图片 ID 列表
        'raw_data': raw_data         # 文本显示数据
    }

    # 5. 重定向到结果页。这是实现页面跳转的关键。
    return redirect(url_for('result_page', session_id=session_id))


# =========================================================================
# 4. 结果路由：根据 ID 查找并渲染结果界面
# =========================================================================
@app.route('/result/<session_id>', methods=['GET'])
def result_page(session_id):
    """
    根据 URL 中的 session_id 查找结果数据，并渲染最终的标签界面。
    """
    # 1. 查找存储的结果
    result_data = SESSION_DATA.get(session_id)

    if not result_data:
        return "error 404", 404

    # 2. 从存储的数据中提取 SVG ID 列表和文本数据
    id_list: List[str] = result_data['element_ids']
    raw_data: Dict[str, str] = result_data['raw_data']
    
    # 3. 准备数据传给 HTML 模板 (将列表/字典数据解包成单个变量)
    context = {
        # SVG 元素 ID: 必须与 mapping.py 中 append 的顺序一致！
        # 假设顺序为：[核心, MBTI, 本科背景, 硕士光环, ...]
        'core_element_id': id_list[0] if len(id_list) > 0 else '',
        'mbti_icon_id': id_list[1] if len(id_list) > 1 else '',
        'background_uni_id': id_list[2] if len(id_list) > 2 else '',
        'halo_uni_id': id_list[3] if len(id_list) > 3 else '',
        'fixed_frame_id': id_list[4] if len(id_list) > 4 else '',
        'bound_salary_id': id_list[5] if len(id_list) > 5 else '', 
        'unit_gbp_id': id_list[6] if len(id_list) > 6 else '', 
        'bound_age_id': id_list[7] if len(id_list) > 7 else '', 
        'bound_country_id': id_list[8] if len(id_list) > 8 else '',
        'major_svg_id': id_list[9] if len(id_list) > 9 else '',
        # 文本显示数据
        'salary_text': raw_data['salary_text'],
        'age_text': raw_data['age_text'],
        'nationality_text': raw_data['nationality_text'],
        'layout_id': raw_data['layout_id']
    }

    # 4. 渲染 templates/result.html，并传入所有动态数据
    return render_template('result.html', **context)


# =========================================================================
# 5. 启动应用
# =========================================================================
if __name__ == '__main__':
    # 运行 Flask 应用。 debug=True 使得代码修改后应用自动重启。
    print("Flask 应用已启动，请访问 http://127.0.0.1:5000")
    app.run(debug=True)