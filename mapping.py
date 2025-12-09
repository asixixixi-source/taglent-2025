# mapping.py
import random
from typing import List, Dict, Any

# 假设您的所有设计元素文件 (SVG/PNG) 都以这些 ID 命名，并放在 static/images 文件夹中。
# 例如：CORE_EXPERT.svg, BG_BLUE.png, MBTI_LEADER.svg 等。

def get_element_ids(salary_expect: int, nationality: str, mbti_type: str, 
                    bachelor_uni: str, master_uni: str, age: int, major: str) -> tuple[List[str], Dict[str, str]]:
    
    selected_ids: List[str] = []

    job_match_score = random.randint(60, 100) 
    
    # 用于随机调取院校关联元素，确保每次运行结果不同
    bachelor_seed = random.randint(1, 4) # 本科随机值
    
   # A. 匹配度
    if job_match_score >= 90:
        selected_ids.append("JOB_91") 
    elif job_match_score >= 86:
        selected_ids.append("JOB_86") 
    elif job_match_score >= 50:
        selected_ids.append("JOB_51")
    else:
        selected_ids.append("JOB_34") 

    #  B. MBTI 元素
    mbti_map = {
        'ENTJ': "MBTI_ENTJ",
        'ENFJ': "MBTI_ENFJ",
        'ENFP': "MBTI_ENFP",
        'ENTP': "MBTI_ENTP",
        'ESFJ': "MBTI_ESFJ",
        'ESFP': "MBTI_ESFP",
        'ESTP': "MBTI_ESTP",
        'ESTJ': "MBTI_ESTJ",
        'INTJ': "MBTI_INTJ",
        'INFJ': "MBTI_INFJ",
        'INFP': "MBTI_INFP",
        'INTP': "MBTI_INTP",
        'ISFJ': "MBTI_ISFJ",
        'ISFP': "MBTI_ISFP",
        'ISTP': "MBTI_ISTP",
        'ISTJ': "MBTI_ISTJ"
    }
    # 使用 .get() 确保即使输入错误，也能返回一个默认 ID
    selected_ids.append(mbti_map.get(mbti_type.upper(), "MBTI_DEFAULT"))

    # C. 布局
    LAYOUT_ID: str
    # 判断是否有硕士经历
    has_master_degree = bool(master_uni.strip()) # 检查字符串是否非空，且去除空格后仍有内容
    
    if has_master_degree:
        # 有硕士经历：从三种布局中随机选择一个
        master_layouts = ["LAYOUT_M_01", "LAYOUT_M_02", "LAYOUT_M_03"]
        LAYOUT_ID = random.choice(master_layouts)
    else:
        # 只有本科经历：使用唯一的本科布局
        LAYOUT_ID = "LAYOUT_B_01"

    # D. 院校随机关联元素 (本科/硕士) 
    # 关联本科院校的背景元素 (基于随机种子)
    selected_ids.append(f"BACHELOR_{bachelor_seed}") 
    
    # 关联硕士院校的光环/纹理元素 (基于随机种子)
    if LAYOUT_ID.startswith("LAYOUT_M"):
        master_svg_id = 'NONE_HALO'
        if master_uni.strip():  
            master_seed = random.randint(1, 4)
            if master_seed % 2 == 0:
                master_svg_id = "MASTER_2"
            else:
                master_svg_id = "MASTER_1"
        selected_ids.append(master_svg_id) 
    else: 
        selected_ids.append("NONE_HALO")
    
    # E. 标签等固定元素
    selected_ids.append("FRAME_FIXED")
    selected_ids.append("BOUND_SALARY")

    if LAYOUT_ID == 'LAYOUT_M_01' or LAYOUT_ID == 'LAYOUT_M_02':
        selected_ids.append("UNIT_GBP2")
    else:
        selected_ids.append("UNIT_GBP1")

    selected_ids.append("BOUND_AGE")
    selected_ids.append("BOUND_COUNTRY")

    # F. 专业
    MAJOR_TO_SVG_MAP = {
        "Arts & Design": "MAJOR_ARTS",
        "STEM": "MAJOR_STEM",
        "Humanities": "MAJOR_HUMANITIES",
        "Business": "MAJOR_BUSINESS",
        "Law": "MAJOR_LAW",
        "Medicine": "MAJOR_MEDICINE",
    }
    
    # 根据用户选择的专业，获取对应的 SVG ID
    major_svg_id = MAJOR_TO_SVG_MAP.get(major, "MAJOR_DEFAULT") # MAJOR_DEFAULT 是以防万一的默认值
    selected_ids.append(major_svg_id)

    # G. 年薪、年龄、国籍
    
    raw_data: Dict[str, str] = {
        'salary_text': f"{salary_expect}",
        'age_text': str(age),
        'nationality_text': str(nationality),
        'layout_id': LAYOUT_ID
    }
    
    # =========================================================================
    # 步骤 3: 返回所有元素 ID
    # =========================================================================
    # 返回一个包含所有计算和匹配结果的 ID 列表
    return selected_ids, raw_data

# -----------------------------------------------------------------------------
# 额外的辅助函数 (可选，用于在本地测试 mapping.py)
# -----------------------------------------------------------------------------
if __name__ == '__main__':
    test_ids, test_data = get_element_ids(
        salary_expect=550000,
        nationality="CN",
        mbti_type="ENTJ",
        bachelor_uni="清华大学",
        master_uni="" ,
        major ="Arts & Design",
        age=32
    )
    print("--- 结果 ID 列表 (用于加载 SVG) ---")
    print(test_ids)
    print("\n--- 原始文本数据 (用于前端显示) ---")
    print(test_data)
    