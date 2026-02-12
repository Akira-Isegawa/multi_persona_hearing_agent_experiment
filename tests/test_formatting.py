"""main.pyのフォーマット関数のテスト."""
import sys
from pathlib import Path

# プロジェクトルートをパスに追加
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from main import (
    format_personas_markdown,
    format_questions_markdown,
    format_interviews_markdown,
)


class TestFormatPersonasMarkdown:
    """format_personas_markdown関数のテスト."""

    def test_format_personas_markdown(self, sample_personas_output):
        """ペルソナをMarkdown形式にフォーマット."""
        result = format_personas_markdown(sample_personas_output)
        
        assert isinstance(result, str)
        assert "# 生成されたペルソナ" in result
        assert sample_personas_output.personas[0].name in result
        assert "年齢" in result
        assert "職業" in result
        assert "背景" in result

    def test_format_personas_markdown_contains_persona_details(self, sample_persona):
        """フォーマット結果にペルソナの詳細が含まれる."""
        from models.schemas import PersonasOutput
        
        output = PersonasOutput(
            personas=[sample_persona],
            generation_rationale="テスト",
        )
        result = format_personas_markdown(output)
        
        assert sample_persona.name in result
        assert str(sample_persona.age) in result
        assert sample_persona.occupation in result
        assert sample_persona.background in result
        
        # ニーズ、行動パターン、痛みポイントも含まれる
        for need in sample_persona.needs:
            assert need in result
        for behavior in sample_persona.behaviors:
            assert behavior in result
        for pain_point in sample_persona.pain_points:
            assert pain_point in result

    def test_format_personas_markdown_with_multiple_personas(self, sample_persona):
        """複数ペルソナのフォーマット."""
        from models.schemas import PersonasOutput
        
        persona2 = sample_persona.model_copy(
            update={"name": "佐藤花子", "age": 28}
        )
        output = PersonasOutput(
            personas=[sample_persona, persona2],
            generation_rationale="テスト",
        )
        result = format_personas_markdown(output)
        
        assert "ペルソナ 1" in result
        assert "ペルソナ 2" in result
        assert sample_persona.name in result
        assert persona2.name in result


class TestFormatQuestionsMarkdown:
    """format_questions_markdown関数のテスト."""

    def test_format_questions_markdown(self, sample_questions_output):
        """質問をMarkdown形式にフォーマット."""
        result = format_questions_markdown(sample_questions_output)
        
        assert isinstance(result, str)
        assert "# 初回ヒアリング質問" in result
        assert "質問リスト" in result
        assert sample_questions_output.questions[0].question in result

    def test_format_questions_markdown_contains_intent(self, sample_interview_question):
        """フォーマット結果に質問の意図が含まれる."""
        from models.schemas import InterviewQuestionsOutput
        
        output = InterviewQuestionsOutput(
            questions=[sample_interview_question],
            design_rationale="テスト",
        )
        result = format_questions_markdown(output)
        
        assert sample_interview_question.question in result
        assert sample_interview_question.intent in result
        assert "*意図*" in result

    def test_format_questions_markdown_with_multiple_questions(self, sample_interview_question):
        """複数質問のフォーマット."""
        from models.schemas import InterviewQuestionsOutput
        
        question2 = sample_interview_question.model_copy(
            update={
                "question": "別の質問",
                "intent": "別の意図",
            }
        )
        output = InterviewQuestionsOutput(
            questions=[sample_interview_question, question2],
            design_rationale="テスト",
        )
        result = format_questions_markdown(output)
        
        assert "質問 1" in result
        assert "質問 2" in result


class TestFormatInterviewsMarkdown:
    """format_interviews_markdown関数のテスト."""

    def test_format_interviews_markdown(self, sample_interview_response):
        """インタビュー結果をMarkdown形式にフォーマット."""
        result = format_interviews_markdown([sample_interview_response])
        
        assert isinstance(result, str)
        assert "# ヒアリング結果" in result
        assert sample_interview_response.persona_name in result
        assert "回答" in result
        assert "重要な洞察" in result

    def test_format_interviews_markdown_contains_answers(self, sample_interview_response):
        """フォーマット結果に回答が含まれる."""
        result = format_interviews_markdown([sample_interview_response])
        
        for answer in sample_interview_response.answers:
            assert answer in result

    def test_format_interviews_markdown_contains_insights(self, sample_interview_response):
        """フォーマット結果に洞察が含まれる."""
        result = format_interviews_markdown([sample_interview_response])
        
        for insight in sample_interview_response.key_insights:
            assert insight in result

    def test_format_interviews_markdown_with_supporting_evidence(self, sample_interview_response):
        """フォーマット結果に裏付け情報が含まれる."""
        result = format_interviews_markdown([sample_interview_response])
        
        if sample_interview_response.supporting_evidence:
            assert "Web検索による裏付け" in result
            for evidence in sample_interview_response.supporting_evidence:
                assert evidence in result

    def test_format_interviews_markdown_without_supporting_evidence(self, sample_persona):
        """裏付け情報なしのインタビュー結果."""
        from models.schemas import InterviewResponse
        
        response = InterviewResponse(
            persona_name=sample_persona.name,
            answers=["回答1"],
            key_insights=["洞察1"],
            supporting_evidence=[],
        )
        result = format_interviews_markdown([response])
        
        # 裏付けセクションはあってもなくてもよい
        assert "ヒアリング結果" in result
        assert sample_persona.name in result

    def test_format_interviews_markdown_with_multiple_interviews(self, sample_interview_response):
        """複数インタビュー結果のフォーマット."""
        response2 = sample_interview_response.model_copy(
            update={"persona_name": "別のペルソナ"}
        )
        result = format_interviews_markdown([sample_interview_response, response2])
        
        assert "1. " in result
        assert "2. " in result
        assert sample_interview_response.persona_name in result
        assert response2.persona_name in result
