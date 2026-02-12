"""複数ペルソナヒアリングのメインワークフロー."""
from typing import Tuple, List
from agents import Runner

from agent_definitions import (
    create_persona_generator_agent,
    create_question_designer_agent,
    create_interviewer_agent,
    create_hypothesis_builder_agent,
    create_validation_question_designer_agent,
    create_question_evaluator_agent,
)
from models.schemas import (
    PersonasOutput,
    PersonaOutput,
    InterviewQuestionsOutput,
    InterviewResponse,
    HypothesisList,
    ValidationQuestionsOutput,
)
from models.evaluation_schemas import (
    EvaluationReport,
)


async def run_multi_persona_hearing_workflow(
    theme: str,
    num_personas: int = 15,
    verbose: bool = True,
) -> Tuple[
    PersonasOutput,
    InterviewQuestionsOutput,
    List[InterviewResponse],
    HypothesisList,
    ValidationQuestionsOutput,
]:
    """
    複数ペルソナヒアリングワークフローを実行する.
    
    Args:
        theme: ヒアリングのテーマ
        num_personas: 生成するペルソナの数（デフォルト: 15）
        verbose: 進捗を表示するか
    
    Returns:
        Tuple containing:
            - PersonasOutput: 生成されたペルソナ
            - InterviewQuestionsOutput: 初回ヒアリング質問
            - List[InterviewResponse]: 各ペルソナへのヒアリング結果
            - HypothesisList: 課題・インサイト仮説
            - ValidationQuestionsOutput: 検証用質問
    """
    if verbose:
        print("=" * 80)
        print("🎯 複数ペルソナヒアリングワークフローを開始します")
        print("=" * 80)
        print(f"テーマ: {theme}")
        print(f"生成ペルソナ数: {num_personas}")
        print()
    
    # フェーズ1: ペルソナ生成
    if verbose:
        print("─" * 80)
        print("📋 フェーズ1: ペルソナ生成")
        print("─" * 80)
    
    persona_generator = create_persona_generator_agent()
    persona_prompt = f"""
以下のテーマについて、{num_personas}体の多様なペルソナを生成してください。

テーマ:
{theme}

要件:
- 多様な年齢、職業、背景を持つペルソナを生成する
- 各ペルソナは独自の視点やニーズを持つ
- テーマに対して異なる関心や経験を持つペルソナを含める
- 極端なケース（先進的/保守的など）も含める
"""
    
    result = await Runner.run(persona_generator, persona_prompt)
    personas_output = result.final_output_as(PersonasOutput)
    
    if verbose:
        print(f"✅ {len(personas_output.personas)}体のペルソナを生成しました")
        for i, persona in enumerate(personas_output.personas, 1):
            print(f"   {i}. {persona.name} ({persona.age}歳, {persona.occupation})")
        print()
    
    # フェーズ2: 初回ヒアリング質問の設計
    if verbose:
        print("─" * 80)
        print("💬 フェーズ2: 初回ヒアリング質問の設計")
        print("─" * 80)
    
    question_designer = create_question_designer_agent()
    question_prompt = f"""
以下のテーマについて、効果的なヒアリング質問を設計してください。

テーマ:
{theme}

生成されたペルソナの概要:
{personas_output.generation_rationale}

要件:
- 10-15問程度の質問を作成する
- オープンエンドな質問を中心にする
- 行動、課題、期待を探る質問を含める
- 各質問の意図を明確にする
"""
    
    result = await Runner.run(question_designer, question_prompt)
    questions_output = result.final_output_as(InterviewQuestionsOutput)
    
    if verbose:
        print(f"✅ {len(questions_output.questions)}個の質問を設計しました")
        print()
    
    # フェーズ3: 各ペルソナへのヒアリング実行
    if verbose:
        print("─" * 80)
        print("🎤 フェーズ3: 各ペルソナへのヒアリング実行")
        print("─" * 80)
    
    interviewer = create_interviewer_agent()
    interviews: List[InterviewResponse] = []
    
    for i, persona in enumerate(personas_output.personas, 1):
        if verbose:
            print(f"   [{i}/{len(personas_output.personas)}] {persona.name} へのヒアリング中...")
        
        # ペルソナ情報と質問を整形
        persona_info = f"""
ペルソナ情報:
- 名前: {persona.name}
- 年齢: {persona.age}歳
- 職業: {persona.occupation}
- 背景: {persona.background}
- ニーズ: {', '.join(persona.needs)}
- 行動パターン: {', '.join(persona.behaviors)}
- 痛みポイント: {', '.join(persona.pain_points)}
"""
        
        questions_text = "\n".join([
            f"{j+1}. {q.question} (意図: {q.intent})"
            for j, q in enumerate(questions_output.questions)
        ])
        
        interview_prompt = f"""
あなたは以下のペルソナになりきって、質問に回答してください。

{persona_info}

質問リスト:
{questions_text}

要件:
- ペルソナの背景や属性を踏まえた回答をする
- 具体的なエピソードや経験を含める
- Web検索を使って、回答内容の現実性を確認し裏付けを取る
- 回答から得られた重要な洞察を抽出する
"""
        
        result = await Runner.run(interviewer, interview_prompt)
        interview = result.final_output_as(InterviewResponse)
        interviews.append(interview)
        
        if verbose:
            print(f"      ✓ 完了 ({len(interview.key_insights)}個の洞察を抽出)")
    
    if verbose:
        print(f"\n✅ {len(interviews)}件のヒアリングを完了しました")
        print()
    
    # フェーズ4: 課題仮説・インサイト仮説の生成
    if verbose:
        print("─" * 80)
        print("💡 フェーズ4: 課題仮説・インサイト仮説の生成")
        print("─" * 80)
    
    hypothesis_builder = create_hypothesis_builder_agent()
    
    # ヒアリング結果を整形
    interviews_summary = []
    for interview in interviews:
        summary = f"""
ペルソナ: {interview.persona_name}
回答: {' / '.join(interview.answers[:3])}...  # 最初の3つの回答
洞察: {' / '.join(interview.key_insights)}
裏付け: {' / '.join(interview.supporting_evidence[:2]) if interview.supporting_evidence else 'なし'}
"""
        interviews_summary.append(summary)
    
    separator = '─' * 40
    interviews_text = f"\n{separator}\n".join(interviews_summary)
    
    hypothesis_prompt = f"""
以下のヒアリング結果を分析し、課題仮説とインサイト仮説を生成してください。

テーマ:
{theme}

ヒアリング結果:
{separator}
{interviews_text}

要件:
- 複数のペルソナから共通して見られるパターンを抽出する
- 検証可能な仮説を立てる
- 各仮説に根拠と確信度を示す
- 課題仮説とインサイト仮説の両方を含める
- 5-10個程度の仮説に絞り込む
"""
    
    result = await Runner.run(hypothesis_builder, hypothesis_prompt)
    hypotheses = result.final_output_as(HypothesisList)
    
    if verbose:
        print(f"✅ 課題仮説 {len(hypotheses.problem_hypotheses)}個、"
              f"インサイト仮説 {len(hypotheses.insight_hypotheses)}個を生成しました")
        print()
    
    # フェーズ5: 仮説検証用のヒアリング項目洗い出し
    if verbose:
        print("─" * 80)
        print("🔍 フェーズ5: 仮説検証用のヒアリング項目洗い出し")
        print("─" * 80)
    
    validation_designer = create_validation_question_designer_agent()
    
    # 仮説を整形
    problem_hyp_text = "\n".join([
        f"- {h.statement} (確信度: {h.confidence_level}/10)"
        for h in hypotheses.problem_hypotheses
    ])
    
    insight_hyp_text = "\n".join([
        f"- {h.statement} (確信度: {h.confidence_level}/10)"
        for h in hypotheses.insight_hypotheses
    ])
    
    validation_prompt = f"""
以下の仮説を検証するための効果的なヒアリング項目を設計してください。

テーマ:
{theme}

課題仮説:
{problem_hyp_text}

インサイト仮説:
{insight_hyp_text}

要件:
- 各仮説を検証できる質問を作成する
- 反証可能な質問を含める
- 優先順位を付ける
- 10-20問程度に絞り込む
"""
    
    result = await Runner.run(validation_designer, validation_prompt)
    validation_questions = result.final_output_as(ValidationQuestionsOutput)
    
    if verbose:
        print(f"✅ {len(validation_questions.questions)}個の検証用質問を設計しました")
        print()
        print("=" * 80)
        print("🎉 ワークフロー完了")
        print("=" * 80)
        print()
    
    return (
        personas_output,
        questions_output,
        interviews,
        hypotheses,
        validation_questions,
    )


async def run_question_evaluation_workflow(
    theme: str,
    initial_questions: InterviewQuestionsOutput,
    validation_questions: ValidationQuestionsOutput,
    hypotheses: HypothesisList,
    verbose: bool = True,
) -> EvaluationReport:
    """
    質問セット評価ワークフローを実行する.
    
    初回ヒアリング質問と検証用ヒアリング質問を比較・評価し、
    質問設計の進化と改善点を分析するレポートを生成する。
    
    Args:
        theme: ヒアリングのテーマ
        initial_questions: 初回ヒアリング質問
        validation_questions: 検証用ヒアリング質問
        hypotheses: 立てられた仮説（コンテキスト情報として使用）
        verbose: 進捗を表示するか
    
    Returns:
        EvaluationReport: 評価レポート
    """
    if verbose:
        print("=" * 80)
        print("📊 質問セット評価ワークフローを開始します")
        print("=" * 80)
        print()
    
    # 質問評価エージェントの作成
    evaluator = create_question_evaluator_agent()
    
    # 評価用プロンプトの作成
    evaluation_prompt = f"""
以下の情報に基づいて、初回ヒアリング質問と検証用ヒアリング質問を比較・評価してください。

## テーマ
{theme}

## 初回ヒアリング質問（15問）
設計の意図:
{initial_questions.design_rationale}

質問リスト:
"""
    
    # 初回質問の詳細を追加
    for i, q in enumerate(initial_questions.questions, 1):
        evaluation_prompt += f"\n{i}. {q.question}\n   意図: {q.intent}"
    
    evaluation_prompt += f"""

## 検証用ヒアリング質問（{len(validation_questions.questions)}問）
検証戦略:
{validation_questions.validation_strategy}

優先順位付け:
"""
    
    # 優先順位を追加
    for i, priority_q in enumerate(validation_questions.priority_order[:5], 1):
        evaluation_prompt += f"\n{i}. {priority_q}"
    
    evaluation_prompt += f"""

全質問リスト:
"""
    
    # 検証質問の詳細を追加
    for i, q in enumerate(validation_questions.questions, 1):
        evaluation_prompt += f"\n{i}. {q.question}\n   意図: {q.intent}"
    
    evaluation_prompt += f"""

## 立てられた仮説の概要
課題仮説: {len(hypotheses.problem_hypotheses)}個
インサイト仮説: {len(hypotheses.insight_hypotheses)}個

統合的サマリー:
{hypotheses.synthesis_summary}

## 評価タスク
以下の側面から、2つの質問セットを総合的に比較・評価してください：

1. **仮説との紐付けの明確さ** - 検証質問は各質問が仮説と明確に対応しているか
2. **反証可能性** - 仮説の棄却を可能にする設計になっているか
3. **中立性への配慮** - 特定ソリューションへの誘導がないか
4. **質問の具体性** - 具体的なケースや実例を求める表現の度合い
5. **深さ・掘り下げ** - 単一質問での深掘り度合い
6. **観点の幅** - 複数のステークホルダー・課題領域をカバーしているか
7. **実用性** - 実施可能性と時間効率

各側面について：
- 初回質問のスコア（0-5）
- 検証質問のスコア（0-5）
- 改善ポイント数
- 詳細説明と具体例

その上で、以下を含む総合レポートを作成してください：
- 両者の強み
- テーマ別のマッピング
- 今後の改善提案
- ハイブリッド版への提案
"""
    
    if verbose:
        print("─" * 80)
        print("📋 質問セット評価分析中...")
        print("─" * 80)
    
    result = await Runner.run(evaluator, evaluation_prompt)
    evaluation_report = result.final_output_as(EvaluationReport)
    
    if verbose:
        print(f"✅ 評価レポートを生成しました")
        print()
        print("主要な評価結果:")
        print(f"  - 初回質問: {evaluation_report.comparison.question_count_initial}問")
        print(f"  - 検証質問: {evaluation_report.comparison.question_count_validation}問")
        print(f"  - 質問数の変化率: {evaluation_report.comparison.count_change_percent:+.1f}%")
        print()
        print("最重要改善ポイント:")
        for i, improvement in enumerate(evaluation_report.key_improvements[:3], 1):
            print(f"  {i}. {improvement}")
        print()
    
    return evaluation_report

