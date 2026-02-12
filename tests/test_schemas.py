"""スキーマのテスト."""
import pytest
from pydantic import ValidationError

from models.schemas import (
    PersonaOutput,
    PersonasOutput,
    InterviewQuestion,
    InterviewQuestionsOutput,
    InterviewResponse,
    HypothesisItem,
    HypothesisList,
    ValidationQuestionsOutput,
)


class TestPersonaOutput:
    """PersonaOutputスキーマのテスト."""

    def test_valid_persona_creation(self, sample_persona: PersonaOutput):
        """正常なペルソナの作成."""
        assert sample_persona.name == "田中太郎"
        assert sample_persona.age == 35
        assert sample_persona.occupation == "ソフトウェアエンジニア"
        assert len(sample_persona.needs) == 2
        assert len(sample_persona.behaviors) == 2
        assert len(sample_persona.pain_points) == 2

    def test_persona_age_validation(self):
        """ペルソナの年齢検証."""
        with pytest.raises(ValidationError):
            PersonaOutput(
                name="太郎",
                age=0,  # 無効な年齢
                occupation="エンジニア",
                background="背景",
                needs=["need1"],
                behaviors=["behavior1"],
                pain_points=["pain1"],
            )

    def test_persona_age_max_validation(self):
        """ペルソナの最大年齢検証."""
        with pytest.raises(ValidationError):
            PersonaOutput(
                name="太郎",
                age=121,  # 120を超える無効な年齢
                occupation="エンジニア",
                background="背景",
                needs=["need1"],
                behaviors=["behavior1"],
                pain_points=["pain1"],
            )

    def test_persona_required_fields(self):
        """ペルソナの必須フィールド検証."""
        with pytest.raises(ValidationError) as exc_info:
            PersonaOutput(
                name="太郎",
                # ageが欠落
                occupation="エンジニア",
                background="背景",
                needs=["need1"],
                behaviors=["behavior1"],
                pain_points=["pain1"],
            )
        assert "age" in str(exc_info.value)


class TestPersonasOutput:
    """PersonasOutputスキーマのテスト."""

    def test_valid_personas_output(self, sample_personas_output: PersonasOutput):
        """正常なペルソナセット出力."""
        assert len(sample_personas_output.personas) > 0
        assert len(sample_personas_output.generation_rationale) > 0

    def test_personas_output_with_multiple_personas(self, sample_persona: PersonaOutput):
        """複数ペルソナを含むセット出力."""
        personas = PersonasOutput(
            personas=[sample_persona] * 3,
            generation_rationale="3体のペルソナを生成しました。",
        )
        assert len(personas.personas) == 3


class TestInterviewQuestion:
    """InterviewQuestionスキーマのテスト."""

    def test_valid_question_creation(self, sample_interview_question: InterviewQuestion):
        """正常な質問の作成."""
        assert len(sample_interview_question.question) > 0
        assert len(sample_interview_question.intent) > 0

    def test_question_required_fields(self):
        """質問の必須フィールド検証."""
        with pytest.raises(ValidationError):
            InterviewQuestion(
                question="質問内容",
                # intentが欠落
            )


class TestInterviewQuestionsOutput:
    """InterviewQuestionsOutputスキーマのテスト."""

    def test_valid_questions_output(
        self, sample_questions_output: InterviewQuestionsOutput
    ):
        """正常な質問セット出力."""
        assert len(sample_questions_output.questions) > 0
        assert len(sample_questions_output.design_rationale) > 0

    def test_questions_count(self, sample_interview_question: InterviewQuestion):
        """複数質問のセット出力."""
        questions = InterviewQuestionsOutput(
            questions=[sample_interview_question] * 5,
            design_rationale="5個の質問を設計しました。",
        )
        assert len(questions.questions) == 5


class TestInterviewResponse:
    """InterviewResponseスキーマのテスト."""

    def test_valid_response_creation(self, sample_interview_response: InterviewResponse):
        """正常な応答の作成."""
        assert sample_interview_response.persona_name == "田中太郎"
        assert len(sample_interview_response.answers) > 0
        assert len(sample_interview_response.key_insights) > 0

    def test_response_with_supporting_evidence(self):
        """裏付け情報を含む応答."""
        response = InterviewResponse(
            persona_name="田中太郎",
            answers=["回答1", "回答2"],
            key_insights=["洞察1", "洞察2"],
            supporting_evidence=["証拠1", "証拠2"],
        )
        assert len(response.supporting_evidence) == 2

    def test_response_without_supporting_evidence(self):
        """裏付け情報なしの応答（デフォルト空リスト）."""
        response = InterviewResponse(
            persona_name="田中太郎",
            answers=["回答1"],
            key_insights=["洞察1"],
        )
        assert response.supporting_evidence == []


class TestHypothesisItem:
    """HypothesisItemスキーマのテスト."""

    def test_valid_hypothesis_creation(self, sample_hypothesis_item: HypothesisItem):
        """正常な仮説の作成."""
        assert sample_hypothesis_item.hypothesis_type == "課題仮説"
        assert len(sample_hypothesis_item.statement) > 0
        assert len(sample_hypothesis_item.evidence) > 0
        assert 1 <= sample_hypothesis_item.confidence_level <= 10

    def test_hypothesis_confidence_level_validation(self):
        """仮説の確信度検証."""
        with pytest.raises(ValidationError):
            HypothesisItem(
                hypothesis_type="課題仮説",
                statement="仮説",
                evidence=["証拠"],
                confidence_level=11,  # 10を超える無効な値
                testable_prediction="予測",
            )

    def test_hypothesis_confidence_level_min_validation(self):
        """仮説の確信度最小値検証."""
        with pytest.raises(ValidationError):
            HypothesisItem(
                hypothesis_type="課題仮説",
                statement="仮説",
                evidence=["証拠"],
                confidence_level=0,  # 1未満の無効な値
                testable_prediction="予測",
            )


class TestHypothesisList:
    """HypothesisListスキーマのテスト."""

    def test_valid_hypotheses_list(self, sample_hypotheses_list: HypothesisList):
        """正常な仮説リスト."""
        assert len(sample_hypotheses_list.problem_hypotheses) > 0
        assert len(sample_hypotheses_list.insight_hypotheses) > 0
        assert len(sample_hypotheses_list.synthesis_summary) > 0

    def test_hypotheses_separation(self, sample_hypothesis_item: HypothesisItem):
        """課題仮説とインサイト仮説の分離."""
        hypotheses = HypothesisList(
            problem_hypotheses=[sample_hypothesis_item],
            insight_hypotheses=[sample_hypothesis_item],
            synthesis_summary="まとめ",
        )
        # 両方のリストが独立している
        assert hypotheses.problem_hypotheses is not hypotheses.insight_hypotheses


class TestValidationQuestionsOutput:
    """ValidationQuestionsOutputスキーマのテスト."""

    def test_valid_validation_questions(
        self, sample_validation_questions: ValidationQuestionsOutput
    ):
        """正常な検証質問セット."""
        assert len(sample_validation_questions.questions) > 0
        assert len(sample_validation_questions.validation_strategy) > 0
        assert len(sample_validation_questions.priority_order) > 0
