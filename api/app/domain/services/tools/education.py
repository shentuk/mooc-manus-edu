#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2025/06/01 10:00
@Author  : EduManus Team
@File    : education.py
"""
from typing import Optional

from app.domain.external.sandbox import Sandbox
from app.domain.models.tool_result import ToolResult
from .base import BaseTool, tool


class EducationTool(BaseTool):
    """教学工具箱，提供课程规划、作业批改、试题生成、学习分析、教案创建等教学能力"""
    name: str = "education"

    def __init__(self, sandbox: Sandbox) -> None:
        """构造函数，完成教学工具箱初始化"""
        super().__init__()
        self.sandbox = sandbox

    @tool(
        name="edu_create_course_outline",
        description="根据学科、年级和教学目标生成完整的课程大纲。生成的大纲包含课程信息、教学目标、单元规划、课时安排等内容，以Markdown格式保存到沙箱文件系统中。适用于教师备课、学期规划或课程设计场景。",
        parameters={
            "subject": {
                "type": "string",
                "description": "学科名称，如'高中数学'、'初中英语'、'小学语文'"
            },
            "grade": {
                "type": "string",
                "description": "年级，如'高一'、'初二'、'三年级'"
            },
            "objectives": {
                "type": "string",
                "description": "教学目标描述，说明学生需要掌握的核心知识和能力"
            },
            "duration": {
                "type": "string",
                "description": "(可选)课程时长，如'一学期'、'16周'、'8课时'，默认为'一学期'"
            },
            "output_path": {
                "type": "string",
                "description": "(可选)输出文件路径，默认为'/home/ubuntu/course_outline.md'"
            }
        },
        required=["subject", "grade", "objectives"],
    )
    async def edu_create_course_outline(
            self,
            subject: str,
            grade: str,
            objectives: str,
            duration: Optional[str] = None,
            output_path: Optional[str] = None,
    ) -> ToolResult:
        """在沙箱中生成课程大纲并保存为Markdown文件"""
        duration = duration or "一学期"
        output_path = output_path or "/home/ubuntu/course_outline.md"

        script_content = f'''
import json

# 课程大纲基本信息
course_info = {{
    "subject": "{subject}",
    "grade": "{grade}",
    "objectives": """{objectives}""",
    "duration": "{duration}",
}}

# 生成Markdown格式的课程大纲
outline_md = f"""# {{course_info["subject"]}} 课程大纲

## 基本信息

- **学科**: {{course_info["subject"]}}
- **年级**: {{course_info["grade"]}}
- **课程时长**: {{course_info["duration"]}}

## 教学目标

{{course_info["objectives"]}}

## 课程大纲框架

> 以下为课程大纲框架，请根据实际教学需求进一步完善各单元的具体内容。

### 第一单元：基础概念导入

**教学目标**: 帮助学生建立本学科的基本概念框架，激发学习兴趣。

**课时安排**: 约占总课时的20%

**教学重点**: 核心概念的理解与初步应用

**教学难点**: 抽象概念的具象化理解

### 第二单元：核心知识讲解

**教学目标**: 系统讲解本课程的核心知识点，建立知识体系。

**课时安排**: 约占总课时的35%

**教学重点**: 核心知识点的掌握与运用

**教学难点**: 知识点之间的关联与综合应用

### 第三单元：深化拓展

**教学目标**: 在掌握基础知识的前提下，进行深化学习和拓展训练。

**课时安排**: 约占总课时的25%

**教学重点**: 知识的深化理解与灵活运用

**教学难点**: 综合性问题的分析与解决

### 第四单元：复习与评价

**教学目标**: 系统复习所学内容，进行阶段性评价。

**课时安排**: 约占总课时的20%

**教学重点**: 知识体系的梳理与巩固

**教学难点**: 查漏补缺，针对性强化

## 教学方法建议

本课程建议采用讲授法与探究式学习相结合的方式，注重课堂互动和实践练习。针对不同学习水平的学生，可适当调整教学节奏和内容深度。

## 评价方式

- 形成性评价：课堂练习、作业、小测验（占比40%）
- 终结性评价：期中考试、期末考试（占比60%）
"""

with open("{output_path}", "w", encoding="utf-8") as f:
    f.write(outline_md)

print(f"课程大纲已成功生成并保存到 {output_path}")
print(f"学科: {{course_info['subject']}}, 年级: {{course_info['grade']}}, 时长: {{course_info['duration']}}")
'''

        # 将脚本保存到沙箱并执行
        script_path = "/home/ubuntu/_edu_outline_gen.py"
        await self.sandbox.write_file(filepath=script_path, content=script_content)
        result = await self.sandbox.exec_command(
            "education", "/home/ubuntu", f"python3 {script_path}"
        )
        return result

    @tool(
        name="edu_grade_assignment",
        description="根据评分标准批改学生作业并生成批改报告。读取学生作业内容，按照提供的评分标准或参考答案进行评分，生成包含分数、评语和改进建议的批改报告。适用于教师批改作业、考试阅卷等场景。",
        parameters={
            "student_answer": {
                "type": "string",
                "description": "学生的作业内容或答案"
            },
            "reference_answer": {
                "type": "string",
                "description": "参考答案或评分标准"
            },
            "subject": {
                "type": "string",
                "description": "(可选)学科名称，用于调整评分风格"
            },
            "max_score": {
                "type": "integer",
                "description": "(可选)满分分值，默认为100"
            },
            "output_path": {
                "type": "string",
                "description": "(可选)批改报告输出路径，默认为'/home/ubuntu/grading_report.md'"
            }
        },
        required=["student_answer", "reference_answer"],
    )
    async def edu_grade_assignment(
            self,
            student_answer: str,
            reference_answer: str,
            subject: Optional[str] = None,
            max_score: Optional[int] = None,
            output_path: Optional[str] = None,
    ) -> ToolResult:
        """在沙箱中批改作业并生成批改报告"""
        max_score = max_score or 100
        subject = subject or "通用"
        output_path = output_path or "/home/ubuntu/grading_report.md"

        # 对字符串进行转义处理
        student_answer_escaped = student_answer.replace('\\', '\\\\').replace("'", "\\'").replace('"', '\\"').replace('\n', '\\n')
        reference_answer_escaped = reference_answer.replace('\\', '\\\\').replace("'", "\\'").replace('"', '\\"').replace('\n', '\\n')

        script_content = f'''
# 作业批改脚本
student_answer = """{student_answer_escaped}"""
reference_answer = """{reference_answer_escaped}"""
subject = "{subject}"
max_score = {max_score}

# 生成批改报告
report_md = f"""# 作业批改报告

## 基本信息

- **学科**: {{subject}}
- **满分**: {{max_score}}分

## 学生答案

{{student_answer}}

## 参考答案

{{reference_answer}}

## 批改结果

> 以下为初步批改框架，具体评分需要结合AI分析进一步细化。

### 评分维度

1. **内容准确性**: 答案是否正确，知识点是否准确
2. **完整性**: 答题是否完整，是否有遗漏
3. **逻辑性**: 解题过程是否清晰，逻辑是否严密
4. **规范性**: 书写是否规范，格式是否正确

### 优点

请AI根据学生答案和参考答案的对比，分析学生答案中的亮点和优秀之处。

### 需要改进的地方

请AI根据学生答案和参考答案的差异，指出需要改进的具体方面。

### 改进建议

请AI根据分析结果，给出具体的、有针对性的改进建议。

---
*本报告由 EduManus 智能教学助手自动生成，仅供参考。*
"""

with open("{output_path}", "w", encoding="utf-8") as f:
    f.write(report_md)

print(f"批改报告已生成并保存到 {output_path}")
print(f"学科: {{subject}}, 满分: {{max_score}}分")
'''

        script_path = "/home/ubuntu/_edu_grade_gen.py"
        await self.sandbox.write_file(filepath=script_path, content=script_content)
        result = await self.sandbox.exec_command(
            "education", "/home/ubuntu", f"python3 {script_path}"
        )
        return result

    @tool(
        name="edu_generate_quiz",
        description="根据知识点、题型和数量要求生成测验题目。支持选择题、填空题、判断题、简答题、计算题等多种题型，生成的试题包含题目、选项（如适用）、标准答案和解析。适用于教师出题、单元测试、练习生成等场景。",
        parameters={
            "topic": {
                "type": "string",
                "description": "知识点或主题，如'二次函数'、'牛顿第二定律'"
            },
            "question_type": {
                "type": "string",
                "description": "题型，可选值: 'choice'(选择题), 'fill'(填空题), 'judge'(判断题), 'short_answer'(简答题), 'calculation'(计算题), 'mixed'(混合题型)"
            },
            "count": {
                "type": "integer",
                "description": "题目数量"
            },
            "difficulty": {
                "type": "string",
                "description": "(可选)难度等级: 'easy'(简单), 'medium'(中等), 'hard'(困难), 默认为'medium'"
            },
            "output_path": {
                "type": "string",
                "description": "(可选)输出文件路径，默认为'/home/ubuntu/quiz.md'"
            }
        },
        required=["topic", "question_type", "count"],
    )
    async def edu_generate_quiz(
            self,
            topic: str,
            question_type: str,
            count: int,
            difficulty: Optional[str] = None,
            output_path: Optional[str] = None,
    ) -> ToolResult:
        """在沙箱中生成测验题目并保存为文件"""
        difficulty = difficulty or "medium"
        output_path = output_path or "/home/ubuntu/quiz.md"

        difficulty_map = {
            "easy": "简单",
            "medium": "中等",
            "hard": "困难"
        }
        difficulty_cn = difficulty_map.get(difficulty, "中等")

        type_map = {
            "choice": "选择题",
            "fill": "填空题",
            "judge": "判断题",
            "short_answer": "简答题",
            "calculation": "计算题",
            "mixed": "混合题型"
        }
        type_cn = type_map.get(question_type, "混合题型")

        script_content = f'''
# 试题生成脚本
topic = "{topic}"
question_type = "{type_cn}"
count = {count}
difficulty = "{difficulty_cn}"

quiz_md = f"""# 测验试题

## 基本信息

- **知识点/主题**: {{topic}}
- **题型**: {{question_type}}
- **题目数量**: {{count}}题
- **难度等级**: {{difficulty}}

---

## 试题部分

> 以下为试题框架，具体题目内容需要AI根据知识点进一步生成。

"""

# 根据题型生成框架
for i in range(1, count + 1):
    quiz_md += f"### 第{{i}}题\\n\\n"
    quiz_md += f"**题目**: [请AI根据「{{topic}}」知识点生成第{{i}}道{{question_type}}]\\n\\n"
    if "{question_type}" == "choice":
        quiz_md += "A. \\nB. \\nC. \\nD. \\n\\n"
    quiz_md += f"**答案**: [标准答案]\\n\\n"
    quiz_md += f"**解析**: [详细解题思路和过程]\\n\\n"
    quiz_md += "---\\n\\n"

quiz_md += """
## 答题卡

| 题号 | 答案 |
|------|------|
"""

for i in range(1, count + 1):
    quiz_md += f"| {{i}} | |\\n"

quiz_md += """
---
*本试题由 EduManus 智能教学助手自动生成，请教师审核后使用。*
"""

with open("{output_path}", "w", encoding="utf-8") as f:
    f.write(quiz_md)

print(f"测验试题已生成并保存到 {output_path}")
print(f"主题: {{topic}}, 题型: {{question_type}}, 数量: {{count}}题, 难度: {{difficulty}}")
'''

        script_path = "/home/ubuntu/_edu_quiz_gen.py"
        await self.sandbox.write_file(filepath=script_path, content=script_content)
        result = await self.sandbox.exec_command(
            "education", "/home/ubuntu", f"python3 {script_path}"
        )
        return result

    @tool(
        name="edu_analyze_learning",
        description="分析学生学习数据并生成学习分析报告。支持分析成绩数据、识别薄弱知识点、生成可视化图表和个性化学习建议。输入可以是成绩数据的文件路径或直接的数据描述。适用于学情分析、期中/期末总结、个性化辅导等场景。",
        parameters={
            "data_description": {
                "type": "string",
                "description": "学习数据描述或数据文件路径。可以是成绩列表、学习记录描述，或CSV/JSON数据文件的路径"
            },
            "subject": {
                "type": "string",
                "description": "(可选)学科名称"
            },
            "analysis_type": {
                "type": "string",
                "description": "(可选)分析类型: 'performance'(成绩分析), 'weakness'(薄弱点分析), 'trend'(趋势分析), 'comprehensive'(综合分析), 默认为'comprehensive'"
            },
            "output_path": {
                "type": "string",
                "description": "(可选)报告输出路径，默认为'/home/ubuntu/learning_report.md'"
            }
        },
        required=["data_description"],
    )
    async def edu_analyze_learning(
            self,
            data_description: str,
            subject: Optional[str] = None,
            analysis_type: Optional[str] = None,
            output_path: Optional[str] = None,
    ) -> ToolResult:
        """在沙箱中分析学习数据并生成报告"""
        subject = subject or "综合"
        analysis_type = analysis_type or "comprehensive"
        output_path = output_path or "/home/ubuntu/learning_report.md"

        type_map = {
            "performance": "成绩分析",
            "weakness": "薄弱点分析",
            "trend": "趋势分析",
            "comprehensive": "综合分析"
        }
        type_cn = type_map.get(analysis_type, "综合分析")

        data_desc_escaped = data_description.replace('\\', '\\\\').replace("'", "\\'").replace('"', '\\"').replace('\n', '\\n')

        script_content = f'''
# 学习分析脚本
data_description = """{data_desc_escaped}"""
subject = "{subject}"
analysis_type = "{type_cn}"

report_md = f"""# 学习分析报告

## 基本信息

- **学科**: {{subject}}
- **分析类型**: {{analysis_type}}
- **数据来源**: {{data_description[:200]}}{"..." if len(data_description) > 200 else ""}

## 分析概述

> 以下为分析报告框架，具体的数据分析和可视化需要AI根据实际数据进一步完成。

### 整体表现

请AI根据提供的学习数据，分析学生/班级的整体学习表现，包括平均分、最高分、最低分、及格率等关键指标。

### 成绩分布

请AI生成成绩分布的统计信息，如有需要可使用Python生成可视化图表。

### 薄弱知识点识别

请AI根据数据分析，识别出学生/班级的薄弱知识点，并按严重程度排序。

### 学习建议

请AI根据分析结果，给出针对性的学习建议和改进方案。

## 后续行动建议

1. 针对薄弱知识点进行专项练习
2. 调整教学策略，加强重点知识的讲解
3. 定期进行阶段性测试，跟踪学习进度

---
*本报告由 EduManus 智能教学助手自动生成，仅供参考。*
"""

with open("{output_path}", "w", encoding="utf-8") as f:
    f.write(report_md)

print(f"学习分析报告已生成并保存到 {output_path}")
print(f"学科: {{subject}}, 分析类型: {{analysis_type}}")
'''

        script_path = "/home/ubuntu/_edu_analysis_gen.py"
        await self.sandbox.write_file(filepath=script_path, content=script_content)
        result = await self.sandbox.exec_command(
            "education", "/home/ubuntu", f"python3 {script_path}"
        )
        return result

    @tool(
        name="edu_create_lesson_plan",
        description="根据主题和教学要求生成标准格式的教案文件。教案包含教学目标（知识与技能、过程与方法、情感态度与价值观）、教学重难点、教学准备、教学过程（导入、新课讲授、练习巩固、课堂小结、作业布置）、板书设计等完整内容。适用于教师备课、公开课准备等场景。",
        parameters={
            "topic": {
                "type": "string",
                "description": "教学主题，如'二次函数的图像与性质'、'The Past Tense'"
            },
            "duration_minutes": {
                "type": "integer",
                "description": "课时时长（分钟），如45、90"
            },
            "teaching_method": {
                "type": "string",
                "description": "(可选)教学方法，如'讲授法'、'探究式学习'、'翻转课堂'，默认为'讲授法与探究式学习相结合'"
            },
            "student_level": {
                "type": "string",
                "description": "(可选)学生水平描述，如'基础较好'、'中等水平'、'基础薄弱'"
            },
            "output_path": {
                "type": "string",
                "description": "(可选)输出文件路径，默认为'/home/ubuntu/lesson_plan.md'"
            }
        },
        required=["topic", "duration_minutes"],
    )
    async def edu_create_lesson_plan(
            self,
            topic: str,
            duration_minutes: int,
            teaching_method: Optional[str] = None,
            student_level: Optional[str] = None,
            output_path: Optional[str] = None,
    ) -> ToolResult:
        """在沙箱中生成教案并保存为Markdown文件"""
        teaching_method = teaching_method or "讲授法与探究式学习相结合"
        student_level = student_level or "中等水平"
        output_path = output_path or "/home/ubuntu/lesson_plan.md"

        script_content = f'''
# 教案生成脚本
topic = "{topic}"
duration = {duration_minutes}
method = "{teaching_method}"
level = "{student_level}"

lesson_plan_md = f"""# 教案：{{topic}}

## 基本信息

| 项目 | 内容 |
|------|------|
| **课题** | {{topic}} |
| **课时** | {{duration}}分钟 |
| **教学方法** | {{method}} |
| **学生水平** | {{level}} |

## 一、教学目标

### 知识与技能目标
通过本节课的学习，学生能够掌握「{{topic}}」的核心概念和基本方法，并能在实际问题中灵活运用。

### 过程与方法目标
通过{{method}}，培养学生的逻辑思维能力、分析问题和解决问题的能力。

### 情感态度与价值观目标
激发学生对本学科的学习兴趣，培养严谨的学习态度和合作探究的精神。

## 二、教学重难点

### 教学重点
- 「{{topic}}」的核心概念理解
- 基本方法和技巧的掌握

### 教学难点
- 抽象概念的理解与应用
- 综合性问题的分析与解决

## 三、教学准备

- **教师准备**: 多媒体课件、教学案例、练习题
- **学生准备**: 预习相关内容、准备笔记本

## 四、教学过程

### 1. 导入环节（约{{duration // 9}}分钟）

**设计意图**: 通过生活实例或问题情境引入新课，激发学生学习兴趣。

**教学活动**:
> 请AI根据「{{topic}}」设计具体的导入活动，可以是生活实例、趣味问题或复习旧知等方式。

### 2. 新课讲授（约{{duration * 4 // 9}}分钟）

**设计意图**: 系统讲解核心知识点，帮助学生建立知识框架。

**教学活动**:
> 请AI根据「{{topic}}」设计具体的讲授内容，包括概念引入、定理推导、例题讲解等环节。注意由浅入深，循序渐进。

### 3. 练习巩固（约{{duration * 2 // 9}}分钟）

**设计意图**: 通过练习帮助学生巩固所学知识，及时发现和纠正错误。

**教学活动**:
> 请AI设计2-3道由易到难的练习题，让学生独立完成后进行讲评。

### 4. 课堂小结（约{{duration // 9}}分钟）

**设计意图**: 帮助学生梳理本节课的知识要点，形成完整的知识体系。

**教学活动**:
> 引导学生回顾本节课的主要内容，总结关键知识点和方法。

### 5. 作业布置（约{{duration // 9}}分钟）

**必做题**: 基础练习，巩固课堂所学
**选做题**: 拓展提高，适合学有余力的学生

## 五、板书设计

```
┌─────────────────────────────────────┐
│           {{topic}}                   │
├─────────────────────────────────────┤
│                                     │
│  一、核心概念                        │
│     [概念定义和关键公式]              │
│                                     │
│  二、方法步骤                        │
│     [解题方法和步骤]                  │
│                                     │
│  三、典型例题                        │
│     [例题和解答过程]                  │
│                                     │
└─────────────────────────────────────┘
```

## 六、教学反思

> 课后填写：本节课的教学效果、学生反馈、需要改进的地方等。

---
*本教案由 EduManus 智能教学助手自动生成，请教师根据实际情况进行调整。*
"""

with open("{output_path}", "w", encoding="utf-8") as f:
    f.write(lesson_plan_md)

print(f"教案已生成并保存到 {output_path}")
print(f"课题: {{topic}}, 课时: {{duration}}分钟, 教学方法: {{method}}")
'''

        script_path = "/home/ubuntu/_edu_lesson_gen.py"
        await self.sandbox.write_file(filepath=script_path, content=script_content)
        result = await self.sandbox.exec_command(
            "education", "/home/ubuntu", f"python3 {script_path}"
        )
        return result