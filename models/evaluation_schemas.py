"""質問セット評価のスキーマ定義."""
from typing import List, Dict, Literal
from pydantic import BaseModel, Field


class QuestionComparison(BaseModel):
    """質問セット間の比較結果."""
    
    theme: str = Field(description="比較対象のテーマ")
    question_count_initial: int = Field(description="初回質問の数")
    question_count_validation: int = Field(description="検証質問の数")
    count_change_percent: float = Field(description="質問数の変化率（%）")


class EvaluationDimension(BaseModel):
    """評価の1つの側面."""
    
    dimension_name: str = Field(description="評価項目の名前（例：質問の具体性）")
    initial_score: float = Field(ge=0, le=5, description="初回質問のスコア（0-5）")
    validation_score: float = Field(ge=0, le=5, description="検証質問のスコア（0-5）")
    improvement_points: float = Field(description="改善ポイント数")
    explanation: str = Field(description="スコア差の理由と詳細説明")
    key_changes: List[str] = Field(description="この側面での主な変化点")


class QuestionMapping(BaseModel):
    """初回質問と検証質問のマッピング."""
    
    topic: str = Field(description="トピック名")
    initial_questions: List[int] = Field(description="初回質問の番号リスト")
    validation_questions: List[int] = Field(description="検証質問の番号リスト")
    depth_level: Literal["同等", "やや向上", "明確な向上", "大幅な向上", "劇的な向上"] = Field(
        description="深化度レベル"
    )
    analysis: str = Field(description="マッピングの分析コメント")


class EvaluationReport(BaseModel):
    """質問セット評価レポート."""
    
    title: str = Field(description="レポートタイトル")
    evaluation_date: str = Field(description="評価日時")
    comparison: QuestionComparison = Field(description="質問セット間の基本比較")
    overall_assessment: str = Field(description="総合評価サマリー")
    evaluation_dimensions: List[EvaluationDimension] = Field(
        description="各評価側面の詳細"
    )
    summary_scores: Dict[str, float] = Field(
        description="各評価項目の総合スコア"
    )
    question_mappings: List[QuestionMapping] = Field(
        description="テーマ別のマッピング"
    )
    key_improvements: List[str] = Field(
        description="最も重要な改善ポイント（優先順位付け）"
    )
    recommendations: List[str] = Field(
        description="今後の改善提案"
    )
    strengths_initial: List[str] = Field(
        description="初回質問の強み"
    )
    strengths_validation: List[str] = Field(
        description="検証質問の強み"
    )
    future_improvements: List[str] = Field(
        description="両者を統合した改善案"
    )
