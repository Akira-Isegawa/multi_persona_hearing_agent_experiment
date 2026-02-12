#!/usr/bin/env python3
"""
複数ペルソナヒアリングシステム

入力されたテーマを元に、複数のペルソナを生成し、
各ペルソナにヒアリングを実施して、課題仮説・インサイト仮説を立て、
仮説検証のためのヒアリング項目を洗い出すシステム。
"""
import os
import sys
import asyncio
import argparse
from pathlib import Path
from typing import List
from dotenv import load_dotenv

from workflows import (
    run_multi_persona_hearing_workflow,
    run_question_evaluation_workflow,
)
from models.schemas import (
    PersonaOutput,
    InterviewQuestion,
    InterviewResponse,
    HypothesisItem,
)


def format_personas_markdown(personas_output) -> str:
    """ペルソナ情報をMarkdown形式に整形."""
    lines = ["# 生成されたペルソナ\n"]
    
    lines.append(f"## 生成の根拠\n\n{personas_output.generation_rationale}\n")
    
    for i, persona in enumerate(personas_output.personas, 1):
        lines.append(f"## ペルソナ {i}: {persona.name}\n")
        lines.append(f"- **年齢**: {persona.age}歳")
        lines.append(f"- **職業**: {persona.occupation}")
        lines.append(f"- **背景**: {persona.background}\n")
        
        lines.append("### ニーズ・課題")
        for need in persona.needs:
            lines.append(f"- {need}")
        lines.append("")
        
        lines.append("### 行動パターン")
        for behavior in persona.behaviors:
            lines.append(f"- {behavior}")
        lines.append("")
        
        lines.append("### 痛みポイント")
        for pain in persona.pain_points:
            lines.append(f"- {pain}")
        lines.append("\n---\n")
    
    return "\n".join(lines)


def format_questions_markdown(questions_output) -> str:
    """ヒアリング質問をMarkdown形式に整形."""
    lines = ["# 初回ヒアリング質問\n"]
    
    lines.append(f"## 質問設計の意図\n\n{questions_output.design_rationale}\n")
    lines.append("## 質問リスト\n")
    
    for i, q in enumerate(questions_output.questions, 1):
        lines.append(f"### 質問 {i}")
        lines.append(f"**{q.question}**\n")
        lines.append(f"*意図*: {q.intent}\n")
    
    return "\n".join(lines)


def format_interviews_markdown(interviews: List[InterviewResponse]) -> str:
    """ヒアリング結果をMarkdown形式に整形."""
    lines = ["# ヒアリング結果\n"]
    
    for i, interview in enumerate(interviews, 1):
        lines.append(f"## {i}. {interview.persona_name}\n")
        
        lines.append("### 回答")
        for j, answer in enumerate(interview.answers, 1):
            lines.append(f"{j}. {answer}")
        lines.append("")
        
        lines.append("### 重要な洞察")
        for insight in interview.key_insights:
            lines.append(f"- {insight}")
        lines.append("")
        
        if interview.supporting_evidence:
            lines.append("### Web検索による裏付け")
            for evidence in interview.supporting_evidence:
                lines.append(f"- {evidence}")
            lines.append("")
        
        lines.append("---\n")
    
    return "\n".join(lines)


def format_hypotheses_markdown(hypotheses) -> str:
    """仮説をMarkdown形式に整形."""
    lines = ["# 課題仮説・インサイト仮説\n"]
    
    lines.append(f"## 全体サマリー\n\n{hypotheses.synthesis_summary}\n")
    
    lines.append("## 課題仮説\n")
    for i, hyp in enumerate(hypotheses.problem_hypotheses, 1):
        lines.append(f"### 課題仮説 {i}")
        lines.append(f"**{hyp.statement}**\n")
        lines.append(f"- **確信度**: {hyp.confidence_level}/10")
        lines.append(f"- **検証可能な予測**: {hyp.testable_prediction}\n")
        
        lines.append("**根拠**:")
        for evidence in hyp.evidence:
            lines.append(f"- {evidence}")
        lines.append("")
    
    lines.append("---\n")
    lines.append("## インサイト仮説\n")
    for i, hyp in enumerate(hypotheses.insight_hypotheses, 1):
        lines.append(f"### インサイト仮説 {i}")
        lines.append(f"**{hyp.statement}**\n")
        lines.append(f"- **確信度**: {hyp.confidence_level}/10")
        lines.append(f"- **検証可能な予測**: {hyp.testable_prediction}\n")
        
        lines.append("**根拠**:")
        for evidence in hyp.evidence:
            lines.append(f"- {evidence}")
        lines.append("")
    
    return "\n".join(lines)


def format_validation_questions_markdown(validation_questions) -> str:
    """検証用質問をMarkdown形式に整形."""
    lines = ["# 仮説検証用ヒアリング項目\n"]
    
    lines.append(f"## 検証戦略\n\n{validation_questions.validation_strategy}\n")
    
    lines.append("## 優先順位")
    for i, priority_item in enumerate(validation_questions.priority_order, 1):
        lines.append(f"{i}. {priority_item}")
    lines.append("\n## 質問リスト\n")
    
    for i, q in enumerate(validation_questions.questions, 1):
        lines.append(f"### 質問 {i}")
        lines.append(f"**{q.question}**\n")
        lines.append(f"*意図*: {q.intent}\n")
    
    return "\n".join(lines)


def format_evaluation_report_markdown(evaluation_report) -> str:
    """評価レポートをMarkdown形式に整形."""
    lines = [f"# {evaluation_report.title}\n"]
    
    lines.append(f"**評価日**: {evaluation_report.evaluation_date}\n")
    
    # 比較サマリー
    lines.append("## 比較サマリー\n")
    lines.append(f"- **初回質問数**: {evaluation_report.comparison.question_count_initial}問")
    lines.append(f"- **検証質問数**: {evaluation_report.comparison.question_count_validation}問")
    lines.append(f"- **質問数の変化率**: {evaluation_report.comparison.count_change_percent:+.1f}%\n")
    
    # 総合評価
    lines.append("## 総合評価\n")
    lines.append(f"{evaluation_report.overall_assessment}\n")
    
    # 評価スコア
    lines.append("## 評価スコア\n")
    for dimension in evaluation_report.evaluation_dimensions:
        lines.append(f"### {dimension.dimension_name}")
        lines.append(f"- **初回質問**: {dimension.initial_score:.1f}/5.0")
        lines.append(f"- **検証質問**: {dimension.validation_score:.1f}/5.0")
        lines.append(f"- **改善度**: {dimension.improvement_points:+.1f}ポイント\n")
        lines.append(f"**説明**: {dimension.explanation}\n")
        lines.append("**主な変化点**:")
        for change in dimension.key_changes:
            lines.append(f"- {change}")
        lines.append("")
    
    # 質問テーマ別マッピング
    lines.append("## テーマ別マッピング\n")
    for mapping in evaluation_report.question_mappings:
        lines.append(f"### {mapping.topic}")
        lines.append(f"- **初回質問**: {', '.join(map(str, mapping.initial_questions))}")
        lines.append(f"- **検証質問**: {', '.join(map(str, mapping.validation_questions))}")
        lines.append(f"- **深化度**: {mapping.depth_level}")
        lines.append(f"**分析**: {mapping.analysis}\n")
    
    # 重要な改善ポイント
    lines.append("## 重要な改善ポイント\n")
    for i, improvement in enumerate(evaluation_report.key_improvements, 1):
        lines.append(f"{i}. {improvement}")
    lines.append("")
    
    # 強みと弱み
    lines.append("## 各質問セットの強み\n")
    lines.append("### 初回質問の強み")
    for strength in evaluation_report.strengths_initial:
        lines.append(f"- {strength}")
    lines.append("")
    lines.append("### 検証質問の強み")
    for strength in evaluation_report.strengths_validation:
        lines.append(f"- {strength}")
    lines.append("")
    
    # 今後の改善提案
    lines.append("## 今後の改善提案\n")
    for i, recommendation in enumerate(evaluation_report.recommendations, 1):
        lines.append(f"{i}. {recommendation}")
    lines.append("")
    
    # ハイブリッド版への提案
    lines.append("## ハイブリッド版への提案\n")
    for improvement in evaluation_report.future_improvements:
        lines.append(f"- {improvement}")
    lines.append("")
    
    return "\n".join(lines)


def save_results(
    output_dir: Path,
    personas_output,
    questions_output,
    interviews,
    hypotheses,
    validation_questions,
    evaluation_report=None,
):
    """結果を複数のMarkdownファイルとして保存."""
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. ペルソナ情報
    personas_md = format_personas_markdown(personas_output)
    (output_dir / "personas.md").write_text(personas_md, encoding="utf-8")
    print(f"✅ ペルソナ情報を保存: {output_dir / 'personas.md'}")
    
    # 2. 初回ヒアリング質問
    questions_md = format_questions_markdown(questions_output)
    (output_dir / "initial_questions.md").write_text(questions_md, encoding="utf-8")
    print(f"✅ 初回質問を保存: {output_dir / 'initial_questions.md'}")
    
    # 3. ヒアリング結果
    interviews_md = format_interviews_markdown(interviews)
    (output_dir / "interview_results.md").write_text(interviews_md, encoding="utf-8")
    print(f"✅ ヒアリング結果を保存: {output_dir / 'interview_results.md'}")
    
    # 4. 仮説
    hypotheses_md = format_hypotheses_markdown(hypotheses)
    (output_dir / "hypotheses.md").write_text(hypotheses_md, encoding="utf-8")
    print(f"✅ 仮説を保存: {output_dir / 'hypotheses.md'}")
    
    # 5. 検証用質問
    validation_md = format_validation_questions_markdown(validation_questions)
    (output_dir / "validation_questions.md").write_text(validation_md, encoding="utf-8")
    print(f"✅ 検証用質問を保存: {output_dir / 'validation_questions.md'}")
    
    # 6. 評価レポート（存在する場合）
    if evaluation_report:
        evaluation_md = format_evaluation_report_markdown(evaluation_report)
        (output_dir / "evaluation.md").write_text(evaluation_md, encoding="utf-8")
        print(f"✅ 評価レポートを保存: {output_dir / 'evaluation.md'}")


def main():
    """メインエントリーポイント."""
    parser = argparse.ArgumentParser(
        description="複数ペルソナヒアリングシステム",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  # テーマを直接指定
  python main.py --theme "新しいSaaSビジネスのアイデア"
  
  # ファイルから読み込み
  python main.py --input inputs/theme.md
  
  # ペルソナ数を指定
  python main.py --theme "リモートワークツール" --num-personas 20
  
  # 出力先を指定
  python main.py --theme "健康管理アプリ" --output-dir outputs/health_app
""",
    )
    
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        "--theme",
        type=str,
        help="ヒアリングのテーマ（直接指定）",
    )
    input_group.add_argument(
        "--input",
        type=str,
        help="テーマが記載されたファイルのパス（Markdown推奨）",
    )
    
    parser.add_argument(
        "--num-personas",
        type=int,
        default=15,
        help="生成するペルソナの数（デフォルト: 15）",
    )
    
    parser.add_argument(
        "--output-dir",
        type=str,
        default="outputs",
        help="出力ディレクトリのパス（デフォルト: outputs）",
    )
    
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="進捗表示を抑制",
    )
    
    args = parser.parse_args()
    
    # 環境変数の読み込み
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ エラー: OPENAI_API_KEY が設定されていません", file=sys.stderr)
        print("   .env ファイルまたは環境変数で設定してください", file=sys.stderr)
        sys.exit(1)
    
    # テーマの取得
    if args.theme:
        theme = args.theme
    else:
        input_path = Path(args.input).expanduser().resolve()
        if not input_path.exists():
            print(f"❌ エラー: 入力ファイルが見つかりません: {input_path}", file=sys.stderr)
            sys.exit(1)
        theme = input_path.read_text(encoding="utf-8")
    
    # 出力ディレクトリの準備
    output_dir = Path(args.output_dir).expanduser().resolve()
    
    verbose = not args.quiet
    
    try:
        # ワークフロー実行
        (
            personas_output,
            questions_output,
            interviews,
            hypotheses,
            validation_questions,
        ) = asyncio.run(
            run_multi_persona_hearing_workflow(
                theme=theme,
                num_personas=args.num_personas,
                verbose=verbose,
            )
        )
        
        # 質問セット評価ワークフロー実行
        evaluation_report = None
        if verbose:
            print()
            print("=" * 80)
            print("📊 質問セット評価を実行します...")
            print("=" * 80)
            print()
        
        try:
            evaluation_report = asyncio.run(
                run_question_evaluation_workflow(
                    theme=theme,
                    initial_questions=questions_output,
                    validation_questions=validation_questions,
                    hypotheses=hypotheses,
                    verbose=verbose,
                )
            )
        except Exception as e:
            if verbose:
                print(f"⚠️ 評価ワークフロー実行時にエラーが発生しました: {e}")
                print("   メインのワークフロー結果は保存されています")
        
        # 結果を保存
        print()
        print("=" * 80)
        print("💾 結果を保存しています...")
        print("=" * 80)
        save_results(
            output_dir,
            personas_output,
            questions_output,
            interviews,
            hypotheses,
            validation_questions,
            evaluation_report=evaluation_report,
        )
        
        print()
        print("=" * 80)
        print("🎉 完了しました！")
        print("=" * 80)
        print(f"出力ディレクトリ: {output_dir}")
        
    except KeyboardInterrupt:
        print("\n❌ ユーザーによって中断されました", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ エラーが発生しました: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
