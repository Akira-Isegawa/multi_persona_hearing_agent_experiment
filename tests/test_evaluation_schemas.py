"""評価スキーマのテスト."""
import pytest
from pydantic import ValidationError

from models.evaluation_schemas import (
    QuestionComparison,
    EvaluationDimension,
    QuestionMapping,
    EvaluationReport,
)


@pytest.fixture
def sample_question_comparison() -> QuestionComparison:
    """サンプル質問比較."""
    return QuestionComparison(
        theme="テーマ",
        question_count_initial=10,
        question_count_validation=12,
        count_change_percent=20.0,
    )


@pytest.fixture
def sample_evaluation_dimension() -> EvaluationDimension:
    """サンプル評価側面."""
    return EvaluationDimension(
        dimension_name="質問の具体性",
        initial_score=3.5,
        validation_score=4.2,
        improvement_points=0.7,
        explanation="検証質問ではより具体的な事例を引き出す質問が増えた",
        key_changes=["具体的なユースケースへの言及が増加", "数値的な質問の追加"],
    )


@pytest.fixture
def sample_question_mapping() -> QuestionMapping:
    """サンプル質問マッピング."""
    return QuestionMapping(
        topic="ツール統合",
        initial_questions=[1, 3, 5],
        validation_questions=[2, 4, 6],
        depth_level="明確な向上",
        analysis="検証質問では具体的なツール組み合わせのニーズを掘り下げている",
    )


@pytest.fixture
def sample_evaluation_report(
    sample_question_comparison: QuestionComparison,
    sample_evaluation_dimension: EvaluationDimension,
    sample_question_mapping: QuestionMapping,
) -> EvaluationReport:
    """サンプル評価レポート."""
    return EvaluationReport(
        title="質問セット評価レポート",
        evaluation_date="2024-01-01",
        comparison=sample_question_comparison,
        overall_assessment="検証質問は初回質問に比べ、より深い掘り下げを実現しています。",
        evaluation_dimensions=[sample_evaluation_dimension],
        summary_scores={"具体性": 4.2, "網羅性": 3.8},
        question_mappings=[sample_question_mapping],
        key_improvements=["具体的な事例の引き出し", "検証可能性の向上"],
        recommendations=["さらに定量的な質問の追加", "ユーザーペインの深掘り"],
        strengths_initial=["広い視点", "開放性"],
        strengths_validation=["具体性", "深さ"],
        future_improvements=["広さと深さのバランス"],
    )


class TestQuestionComparison:
    """QuestionComparisonスキーマのテスト."""

    def test_valid_comparison_creation(self, sample_question_comparison: QuestionComparison):
        """正常な比較の作成."""
        assert sample_question_comparison.theme == "テーマ"
        assert sample_question_comparison.question_count_initial == 10
        assert sample_question_comparison.question_count_validation == 12

    def test_comparison_count_change_percent(self, sample_question_comparison: QuestionComparison):
        """比較の変化率計算."""
        # 10から12への変化は 20% 増加
        expected = ((12 - 10) / 10) * 100
        assert sample_question_comparison.count_change_percent == expected


class TestEvaluationDimension:
    """EvaluationDimensionスキーマのテスト."""

    def test_valid_dimension_creation(self, sample_evaluation_dimension: EvaluationDimension):
        """正常な評価側面の作成."""
        assert sample_evaluation_dimension.dimension_name == "質問の具体性"
        assert 0 <= sample_evaluation_dimension.initial_score <= 5
        assert 0 <= sample_evaluation_dimension.validation_score <= 5

    def test_dimension_score_validation(self):
        """評価側面のスコア検証（範囲外）."""
        with pytest.raises(ValidationError):
            EvaluationDimension(
                dimension_name="テスト",
                initial_score=6,  # 5を超える無効な値
                validation_score=4,
                improvement_points=0,
                explanation="説明",
                key_changes=[],
            )

    def test_dimension_score_improvement_calculation(self, sample_evaluation_dimension: EvaluationDimension):
        """改善ポイントの計算."""
        expected_improvement = sample_evaluation_dimension.validation_score - sample_evaluation_dimension.initial_score
        assert abs(sample_evaluation_dimension.improvement_points - expected_improvement) < 0.01


class TestQuestionMapping:
    """QuestionMappingスキーマのテスト."""

    def test_valid_mapping_creation(self, sample_question_mapping: QuestionMapping):
        """正常なマッピングの作成."""
        assert sample_question_mapping.topic == "ツール統合"
        assert len(sample_question_mapping.initial_questions) == 3
        assert len(sample_question_mapping.validation_questions) == 3

    def test_mapping_depth_level_validation(self):
        """マッピングの深化度レベル検証."""
        valid_levels = ["同等", "やや向上", "明確な向上", "大幅な向上", "劇的な向上"]
        
        for level in valid_levels:
            mapping = QuestionMapping(
                topic="テスト",
                initial_questions=[1],
                validation_questions=[2],
                depth_level=level,
                analysis="分析",
            )
            assert mapping.depth_level == level

    def test_mapping_invalid_depth_level(self):
        """マッピングの無効な深化度レベル."""
        with pytest.raises(ValidationError):
            QuestionMapping(
                topic="テスト",
                initial_questions=[1],
                validation_questions=[2],
                depth_level="無効なレベル",  # 無効な値
                analysis="分析",
            )


class TestEvaluationReport:
    """EvaluationReportスキーマのテスト."""

    def test_valid_report_creation(self, sample_evaluation_report: EvaluationReport):
        """正常なレポートの作成."""
        assert sample_evaluation_report.title == "質問セット評価レポート"
        assert sample_evaluation_report.evaluation_date == "2024-01-01"
        assert len(sample_evaluation_report.evaluation_dimensions) > 0
        assert len(sample_evaluation_report.key_improvements) > 0

    def test_report_contains_required_sections(self, sample_evaluation_report: EvaluationReport):
        """レポートが必要なセクションを含む."""
        assert sample_evaluation_report.comparison is not None
        assert sample_evaluation_report.overall_assessment is not None
        assert sample_evaluation_report.evaluation_dimensions is not None
        assert sample_evaluation_report.question_mappings is not None

    def test_report_recommendations_are_present(self, sample_evaluation_report: EvaluationReport):
        """レポートに推奨事項が含まれる."""
        assert len(sample_evaluation_report.recommendations) > 0
        for recommendation in sample_evaluation_report.recommendations:
            assert isinstance(recommendation, str)
            assert len(recommendation) > 0

    def test_report_summary_scores_structure(self, sample_evaluation_report: EvaluationReport):
        """レポートのサマリースコアの構造."""
        assert isinstance(sample_evaluation_report.summary_scores, dict)
        for key, value in sample_evaluation_report.summary_scores.items():
            assert isinstance(key, str)
            assert isinstance(value, (int, float))


class TestEvaluationDataIntegrity:
    """評価スキーマのデータ整合性テスト."""

    def test_dimension_scores_consistency(self, sample_evaluation_dimension: EvaluationDimension):
        """評価側面のスコア一貫性."""
        improvement = sample_evaluation_dimension.validation_score - sample_evaluation_dimension.initial_score
        assert abs(improvement - sample_evaluation_dimension.improvement_points) < 0.01

    def test_report_mappings_reference_valid_questions(self, sample_evaluation_report: EvaluationReport):
        """レポートのマッピングが有効な質問を参照."""
        for mapping in sample_evaluation_report.question_mappings:
            # 質問番号が正の整数である
            assert all(isinstance(q, int) and q > 0 for q in mapping.initial_questions)
            assert all(isinstance(q, int) and q > 0 for q in mapping.validation_questions)
