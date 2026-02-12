"""エージェント定義のテスト."""
import pytest
from unittest.mock import Mock, patch, AsyncMock

from agent_definitions import (
    create_persona_generator_agent,
    create_question_designer_agent,
)


class TestPersonaGeneratorAgent:
    """ペルソナ生成エージェントのテスト."""

    def test_agent_creation(self):
        """エージェントが正常に作成される."""
        agent = create_persona_generator_agent()
        
        assert agent is not None
        assert agent.name == "PersonaGenerator"
        assert len(agent.instructions) > 0

    def test_agent_has_correct_output_type(self):
        """エージェントが正しい出力型を持つ."""
        from models.schemas import PersonasOutput
        
        agent = create_persona_generator_agent()
        
        # エージェントの出力型がPersonasOutputである
        assert agent.output_type == PersonasOutput


class TestQuestionDesignerAgent:
    """質問設計エージェントのテスト."""

    def test_agent_creation(self):
        """エージェントが正常に作成される."""
        agent = create_question_designer_agent()
        
        assert agent is not None
        assert agent.name == "QuestionDesigner"
        assert len(agent.instructions) > 0

    def test_agent_has_correct_output_type(self):
        """エージェントが正しい出力型を持つ."""
        from models.schemas import InterviewQuestionsOutput
        
        agent = create_question_designer_agent()
        
        # エージェントの出力型がInterviewQuestionsOutputである
        assert agent.output_type == InterviewQuestionsOutput

    def test_agent_instructions_mention_open_ended_questions(self):
        """エージェントの指示にオープンエンド質問についての記載がある."""
        agent = create_question_designer_agent()
        
        # 指示内容にオープンエンドな質問についての説明がある
        assert "オープンエンド" in agent.instructions or "終わり" in agent.instructions


class TestAgentImports:
    """エージェント定義のインポートテスト."""

    def test_all_agents_can_be_imported(self):
        """すべてのエージェントがインポートできる."""
        from agent_definitions import (
            create_persona_generator_agent,
            create_question_designer_agent,
            create_interviewer_agent,
            create_hypothesis_builder_agent,
            create_validation_question_designer_agent,
            create_question_evaluator_agent,
        )
        
        # すべてが正常に importできる
        assert callable(create_persona_generator_agent)
        assert callable(create_question_designer_agent)
        assert callable(create_interviewer_agent)
        assert callable(create_hypothesis_builder_agent)
        assert callable(create_validation_question_designer_agent)
        assert callable(create_question_evaluator_agent)

    def test_all_agents_return_agent_instance(self):
        """すべてのエージェントがAgentインスタンスを返す."""
        from agent_definitions import (
            create_persona_generator_agent,
            create_question_designer_agent,
        )
        from agents import Agent
        
        persona_agent = create_persona_generator_agent()
        question_agent = create_question_designer_agent()
        
        assert isinstance(persona_agent, Agent)
        assert isinstance(question_agent, Agent)
