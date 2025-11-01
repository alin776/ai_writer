"""
质量评估模块测试配置
"""

import pytest
from unittest.mock import Mock, AsyncMock


@pytest.fixture
def mock_ai_service():
    """模拟AI服务"""
    service = Mock()
    service.call_llm = AsyncMock(return_value="分数: 8.0\n理由: 内容质量良好")
    return service


@pytest.fixture
def sample_content():
    """示例内容"""
    return """
    林凡站在修仙界的山巅,俯瞰着下方的云海。

    三年前,他还只是一个普通的外门弟子,被所有人嘲笑。但现在,他已经成为了金丹期的强者。

    "师兄,我们终于找到了传说中的神器!"身后传来了小师妹激动的声音。

    林凡微微一笑,转过身来。在小师妹手中,正握着一柄散发着金光的古剑。

    "很好,有了这把剑,我们就能够对抗魔教了。"林凡接过古剑,感受着其中蕴含的强大力量。
    """


@pytest.fixture
def sample_context():
    """示例评估上下文"""
    from backend.app.services.agent.quality.quality_types import EvaluationContext

    return EvaluationContext(
        user_id="test_user",
        novel_id="test_novel",
        chapter_id="test_chapter",
        previous_content="林凡刚刚突破到金丹期,正在巩固修为。",
        outline="主角获得神器,准备对抗魔教",
        writing_style="玄幻修仙风格",
        target_length=500,
        genre="玄幻"
    )
