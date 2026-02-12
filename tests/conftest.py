"""共有フィクスチャと設定."""
import sys
from pathlib import Path
import pytest
from typing import List

# プロジェクトルートをPythonパスに追加
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

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


@pytest.fixture
def sample_persona() -> PersonaOutput:
    """サンプルペルソナ."""
    return PersonaOutput(
        name="田中太郎",
        age=35,
        occupation="ソフトウェアエンジニア",
        background="大手IT企業で10年働いているベテランエンジニア",
        needs=["効率的な開発ツール", "チームコラボレーション"],
        behaviors=["毎日1時間以上コード作成", "週に2回ミーティング"],
        pain_points=["コミュニケーションオーバーヘッド", "ツール切り替えの手間"],
    )


@pytest.fixture
def sample_personas_output(sample_persona: PersonaOutput) -> PersonasOutput:
    """サンプルペルソナセット出力."""
    return PersonasOutput(
        personas=[sample_persona],
        generation_rationale="15体の多様なペルソナを生成しました。年齢、職業、背景の多様性を確保しています。",
    )


@pytest.fixture
def sample_interview_question() -> InterviewQuestion:
    """サンプル面接質問."""
    return InterviewQuestion(
        question="現在、どのようなツールを使用していますか？",
        intent="ユーザーの現在のツール環境を理解する",
    )


@pytest.fixture
def sample_questions_output(
    sample_interview_question: InterviewQuestion,
) -> InterviewQuestionsOutput:
    """サンプル質問セット出力."""
    return InterviewQuestionsOutput(
        questions=[sample_interview_question],
        design_rationale="テーマに基づいて、10個の効果的なヒアリング質問を設計しました。",
    )


@pytest.fixture
def sample_interview_response(sample_persona: PersonaOutput) -> InterviewResponse:
    """サンプル面接応答."""
    return InterviewResponse(
        persona_name=sample_persona.name,
        answers=[
            "主にVSCodeとGitHub Actionsを使っています。",
            "週に2-3回は新しいツールを試しています。",
        ],
        key_insights=[
            "ユーザーはツール選択に時間を費やしている",
            "統合性が重要だと考えている",
        ],
        supporting_evidence=[
            "Stack Overflow 2024 Surveyでも同様の傾向が報告されている",
        ],
    )


@pytest.fixture
def sample_hypothesis_item() -> HypothesisItem:
    """サンプル仮説."""
    return HypothesisItem(
        hypothesis_type="課題仮説",
        statement="開発者はツール統合の不足による作業効率の低下に悩んでいる",
        evidence=[
            "インタビュー対象者全員がツール切り替えの手間を挙げた",
            "業界基準レポートでも同様の課題が報告されている",
        ],
        confidence_level=8,
        testable_prediction="統合ツールの導入で作業効率が30%以上向上する",
    )


@pytest.fixture
def sample_hypotheses_list(sample_hypothesis_item: HypothesisItem) -> HypothesisList:
    """サンプル仮説リスト."""
    return HypothesisList(
        problem_hypotheses=[sample_hypothesis_item],
        insight_hypotheses=[sample_hypothesis_item],
        synthesis_summary="ヒアリング結果から、ツール統合の重要性が明らかになった。",
    )


@pytest.fixture
def sample_validation_questions(
    sample_interview_question: InterviewQuestion,
) -> ValidationQuestionsOutput:
    """サンプル検証質問."""
    return ValidationQuestionsOutput(
        questions=[sample_interview_question],
        validation_strategy="仮説を検証するために、ツール統合の具体的なニーズを深掘りする。",
        priority_order=["ツール統合の具体的なニーズ", "コスト面での考慮"],
    )


@pytest.fixture
def sample_theme() -> str:
    """サンプルテーマ."""
    return "開発者向けの新しいコラボレーションツール"
