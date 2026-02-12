# 質問セット評価機能の統合 - 実装ガイド

## 概要

`multi_persona_hearing`ワークフローに質問セット評価機能を統合しました。初回ヒアリング質問と仮説検証用質問を自動比較・評価し、質問設計の進化を分析するレポートを生成します。

## 実装内容

### 1. 新規ファイル

#### `models/evaluation_schemas.py`
質問評価に関するデータスキーマを定義しています：
- `QuestionComparison`: 質問セット間の基本比較（数、変化率）
- `EvaluationDimension`: 評価項目ごとのスコアと詳細分析
- `QuestionMapping`: テーマ別の質問対応関係
- `EvaluationReport`: 総合評価レポート（メインの出力）

#### `agent_definitions/question_evaluator.py`
質問評価エージェントを定義しています：
- `create_question_evaluator_agent()`: 評価用エージェントの作成
- 仮説との紐付け、反証可能性、中立性などの7つの評価項目を処理
- LLMを用いた自動評価と定量スコアリング

### 2. 修正したファイル

#### `workflows/multi_hearing.py`
- インポートに `create_question_evaluator_agent` と `EvaluationReport` を追加
- 新しい関数 `run_question_evaluation_workflow()` を実装
  - 初回質問、検証質問、仮説を入力として受け取る
  - LLMを使用して総合評価を生成
  - `EvaluationReport` を返す

#### `workflows/__init__.py`
- `run_question_evaluation_workflow` をエクスポート

#### `agent_definitions/__init__.py`
- `create_question_evaluator_agent` をエクスポート

#### `models/__init__.py`
- 評価スキーマのクラスをエクスポート

#### `main.py`
- インポートに評価ワークフロー関数を追加
- `format_evaluation_report_markdown()`: 評価レポートのMarkdown整形
- メイン関数内に評価ワークフロー実行ロジックを追加
  - 通常ワークフロー実行後、自動的に評価ワークフローを実行
  - エラーハンドリングで評価失敗時も他の結果は保存
- `save_results()` に評価レポート保存機能を追加

#### `USAGE.md`
- 新機能の説明を追加
- 評価機能の出力内容を記載
- 評価項目の詳細説明を追加

## 実行フロー

```
main.py
  ↓
run_multi_persona_hearing_workflow()
  ├─ ペルソナ生成
  ├─ 初回質問設計
  ├─ インタビュー実施
  ├─ 仮説生成
  └─ 検証質問設計
  ↓
run_question_evaluation_workflow()  ← 【新規追加】
  ├─ 質問エージェント作成
  ├─ 評価プロンプト構築
  └─ LLMによる総合評価実施
  ↓
save_results()
  └─ 全結果（+evaluation.md）を保存
```

## 出力ファイル

実行後、出力ディレクトリに以下が生成されます：

1. `personas.md` - ペルソナ情報
2. `initial_questions.md` - 初回質問
3. `interview_results.md` - インタビュー結果
4. `hypotheses.md` - 立てられた仮説
5. `validation_questions.md` - 検証用質問
6. **`evaluation.md` - 質問セット評価レポート** ← 新規

## 評価内容（evaluation.md）

### 提供される情報

1. **比較サマリー**
   - 初回質問数と検証質問数
   - 質問数の変化率（%）

2. **総合評価**
   - 質問設計の進化についての概括的評価

3. **詳細スコア（7項目）**
   - 仮説との紐付けの明確さ
   - 反証可能性（科学的厳密性）
   - 中立性への配慮
   - 質問の具体性
   - 深さ・掘り下げ
   - 観点の幅
   - 実用性

   各項目について：
   - 初回質問のスコア（0-5）
   - 検証質問のスコア（0-5）
   - 改善ポイント数
   - 詳細説明
   - 主な変化点

4. **テーマ別マッピング**
   - 各テーマ内での質問の対応関係
   - 深化度レベル
   - テーマ別の分析コメント

5. **重要な改善ポイント**
   - 優先順位付けされたトップ3の改善ポイント

6. **強みと弱み分析**
   - 初回質問の強み
   - 検証質問の強み

7. **改善提案**
   - 実装可能な具体的な改善案
   - ハイブリッド版への提案

## 使用例

### 基本実行（評価含む）
```bash
python main.py --input inputs/theme_example.md
```

→ 6つのファイルが生成され、evaluation.mdが自動生成されます

### 出力ディレクトリを指定
```bash
python main.py \
  --theme "新しいSaaSビジネスのアイデア" \
  --output-dir outputs/my_evaluation
```

→ my_evaluationディレクトリに全結果が保存されます

## エラーハンドリング

評価ワークフロー実行時にエラーが発生した場合：
- メインのワークフロー結果は正常に保存されます
- `evaluation.md` は生成されませんが、他の5つのファイルはすべて利用可能です
- コンソール出力に警告メッセージが表示されます

## パフォーマンス

- **メインワークフロー**: 通常の実行時間（ペルソナ生成、インタビューなど）
- **評価ワークフロー**: 追加で約30-60秒（LLM呼び出し1回）
- **トータル**: メインワークフロー時間 + 約30-60秒

## 拡張性

### 新しい評価項目の追加方法

1. `evaluation_schemas.py` の `EvaluationDimension` は既に拡張可能
2. `question_evaluator.py` のプロンプトに新しい評価項目を追加
3. 返却される `EvaluationReport` に新フィールドを追加

### カスタマイズ

評価エージェントのプロンプト（`question_evaluator.py`）を編集することで：
- 評価項目の重み付け変更
- 言語変更（日本語 ↔ 英語など）
- 業界・用途別のカスタマイズ

## 統合テスト

実装の検証に以下を実行してください：

```bash
python main.py \
  --input inputs/theme_example.md \
  --output-dir outputs/test_evaluation
```

期待される結果：
- ✅ 6つのMarkdownファイルが生成される
- ✅ `evaluation.md` が含まれている
- ✅ 各ファイルが正しいMarkdown形式である
- ✅ スコアと評価内容が論理的に整合している

## 今後の拡張案

1. **CLI コマンド追加**
   - 独立した `evaluate` コマンド（既存ファイルから新規評価）
   - 複数テーマの一括評価

2. **レポート出力形式の拡張**
   - HTML版レポート生成
   - JSON形式でのスコア出力

3. **比較機能の強化**
   - 複数の質問セット同時比較
   - 時系列での評価追跡

4. **インタラクティブ機能**
   - ユーザーが特定の評価項目を強調表示できる機能
   - フィードバックに基づいた再評価

## トラブルシューティング

### 評価ワークフローがスキップされる
原因: LLM呼び出しエラー
→ OpenAI APIキーと接続を確認してください

### 評価スコアが予期と異なる
原因: LLMの出力がスキーマに適合していない可能性
→ `question_evaluator.py` のプロンプトを確認し、出力形式を調整してください

### evaluation.mdが生成されない
原因: エラーハンドリングにより評価が実行されなかった
→ コンソールのエラーメッセージを確認し、問題を解決してください
