"""データスキーマの定義."""
from typing import List
from pydantic import BaseModel, Field


class PersonaOutput(BaseModel):
    """生成された1つのペルソナ."""
    
    name: str = Field(description="ペルソナの名前")
    age: int = Field(ge=1, le=120, description="年齢")
    occupation: str = Field(description="職業")
    background: str = Field(description="背景・属性の詳細説明")
    needs: List[str] = Field(description="ニーズや課題のリスト")
    behaviors: List[str] = Field(description="行動パターンや習慣のリスト")
    pain_points: List[str] = Field(description="痛みポイントや不満のリスト")


class PersonasOutput(BaseModel):
    """複数のペルソナ生成結果."""
    
    personas: List[PersonaOutput] = Field(description="生成されたペルソナのリスト")
    generation_rationale: str = Field(description="ペルソナ生成の根拠と多様性の説明")


class InterviewQuestion(BaseModel):
    """ヒアリング用の質問."""
    
    question: str = Field(description="質問内容")
    intent: str = Field(description="質問の意図・目的")


class InterviewQuestionsOutput(BaseModel):
    """ヒアリング質問セット."""
    
    questions: List[InterviewQuestion] = Field(description="質問のリスト")
    design_rationale: str = Field(description="質問設計の意図と全体戦略")


class InterviewResponse(BaseModel):
    """ペルソナへのヒアリング結果."""
    
    persona_name: str = Field(description="回答したペルソナの名前")
    answers: List[str] = Field(description="各質問に対する回答のリスト")
    key_insights: List[str] = Field(description="回答から得られた重要な洞察のリスト")
    supporting_evidence: List[str] = Field(
        default_factory=list,
        description="Web検索で得られた裏付け情報のリスト"
    )


class HypothesisItem(BaseModel):
    """1つの仮説."""
    
    hypothesis_type: str = Field(description="仮説のタイプ（課題仮説/インサイト仮説）")
    statement: str = Field(description="仮説文")
    evidence: List[str] = Field(description="仮説を裏付ける根拠のリスト")
    confidence_level: int = Field(
        ge=1, le=10,
        description="確信度（1-10、10が最も高い）"
    )
    testable_prediction: str = Field(description="検証可能な予測")


class HypothesisList(BaseModel):
    """課題仮説・インサイト仮説のリスト."""
    
    problem_hypotheses: List[HypothesisItem] = Field(
        description="課題仮説のリスト"
    )
    insight_hypotheses: List[HypothesisItem] = Field(
        description="インサイト仮説のリスト"
    )
    synthesis_summary: str = Field(
        description="全体の統合的なサマリー"
    )


class ValidationQuestionsOutput(BaseModel):
    """仮説検証用のヒアリング項目."""
    
    questions: List[InterviewQuestion] = Field(
        description="検証用質問のリスト"
    )
    validation_strategy: str = Field(
        description="検証戦略の説明"
    )
    priority_order: List[str] = Field(
        description="優先順位付けされた質問内容のリスト"
    )
