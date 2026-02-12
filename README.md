# 複数ペルソナヒアリングシステム

OpenAI Agent SDKを用いた、複数ペルソナへのヒアリングと仮説生成を自動化するシステムです。

## 概要

このシステムは、入力されたテーマを元に以下の作業を自動的に実行します:

1. **ペルソナ生成**: ヒアリング対象となる多様なペルソナを複数生成（デフォルト15体）
2. **初回ヒアリング実行**: 各ペルソナに対してヒアリングを実施（Web Searchで裏付けを取得）
3. **仮説生成**: ヒアリング結果から課題仮説・インサイト仮説を立案
4. **検証項目洗い出し**: 仮説検証のための追加ヒアリング項目を設計

## 特徴

- **OpenAI公式Web Search統合**: ペルソナの発言内容をWeb検索で裏付け
- **多様なペルソナ生成**: デフォルト15体の異なる背景を持つペルソナを生成
- **構造化された出力**: Pydanticスキーマによる型安全な出力
- **複数ファイル出力**: 各フェーズの結果を個別のMarkdownファイルとして保存
- **✨ 質問セット評価機能（新）**: 初回質問と検証質問を自動比較・評価するレポート生成

## 必要要件

- Python 3.10以上
- OpenAI API キー

## インストール

```bash
# 依存関係のインストール
pip install -r requirements.txt
```

## 使用方法

### 基本的な使い方

```bash
# テーマを直接指定
python main.py --theme "新しいSaaSビジネスのアイデア"

# ファイルから読み込み
python main.py --input inputs/theme_example.md

# ペルソナ数を指定（デフォルト: 15）
python main.py --theme "リモートワークツール" --num-personas 20

# 出力先を指定
python main.py --theme "健康管理アプリ" --output-dir outputs/health_app

# 進捗表示を抑制
python main.py --theme "教育プラットフォーム" --quiet
```

### 環境変数の設定

`.env` ファイルをプロジェクトルートに作成し、以下を設定してください:

```
OPENAI_API_KEY=your_api_key_here
```

## 出力ファイル

実行すると、指定した出力ディレクトリ（デフォルト: `outputs/`）に以下のファイルが生成されます:

1. **personas.md**: 生成されたペルソナの詳細情報
2. **initial_questions.md**: 初回ヒアリング用の質問リスト
3. **interview_results.md**: 各ペルソナへのヒアリング結果と洞察
4. **hypotheses.md**: 課題仮説・インサイト仮説
5. **validation_questions.md**: 仮説検証用のヒアリング項目
6. **✨ evaluation.md（新）**: 初回質問と検証質問の比較評価レポート

## プロジェクト構造

```
./
├── main.py                         # CLIエントリーポイント
├── README.md                       # このファイル
├── USAGE.md                        # 詳細な使用方法
├── IMPLEMENTATION_GUIDE.md         # 実装の詳細ガイド（新）
├── __init__.py
├── models/
│   ├── __init__.py
│   ├── schemas.py                  # Pydanticデータモデル定義
│   └── evaluation_schemas.py       # 評価用スキーマ定義（新）
├── agent_definitions/
│   ├── __init__.py
│   ├── persona_generator.py       # ペルソナ生成エージェント
│   ├── question_designer.py       # 質問設計エージェント
│   ├── interviewer.py             # ヒアリング実行エージェント
│   ├── hypothesis_builder.py      # 仮説生成エージェント
│   ├── validation_question_designer.py  # 検証用質問設計エージェント
│   └── question_evaluator.py      # 質問評価エージェント（新）
├── workflows/
│   ├── __init__.py
│   └── multi_hearing.py           # メインワークフロー + 評価ワークフロー（新）
├── inputs/
│   └── theme_example.md           # サンプル入力ファイル
└── outputs/                        # 出力ファイルディレクトリ
```

## ワークフローの詳細

### フェーズ1: ペルソナ生成
- 入力されたテーマに基づき、多様な背景を持つペルソナを生成
- 年齢、職業、ニーズ、行動パターン、痛みポイントを定義
- デフォルトで15体のペルソナを生成

### フェーズ2: 質問設計
- テーマに関連する効果的なヒアリング質問を設計
- オープンエンドな質問を中心に10-15問を作成
- 各質問の意図を明確化

### フェーズ3: ヒアリング実行
- 各ペルソナになりきって質問に回答
- OpenAI公式のWeb Search APIを使用して回答の裏付けを取得
- 重要な洞察を抽出

### フェーズ4: 仮説生成
- ヒアリング結果を横断的に分析
- 課題仮説とインサイト仮説を生成
- 各仮説に確信度と根拠を付与

### フェーズ5: 検証項目洗い出し
- 仮説を検証するための追加ヒアリング項目を設計
- 優先順位を付けて10-20問を提示

### ✨ フェーズ6: 質問セット評価（新）
- 初回質問と検証質問を自動比較
- 仮説との紐付け、反証可能性、中立性など7つの評価項目でスコアリング
- テーマ別のマッピングと改善提案を生成
- 総合評価レポート（evaluation.md）を出力

## カスタマイズ

### ペルソナ数の変更
`--num-personas` オプションでペルソナ数を変更できます:

```bash
python main.py --theme "テーマ" --num-personas 10
```

### エージェントの調整
各エージェントの動作は `agent_definitions/` ディレクトリ内のファイルで調整できます。
`instructions` 部分を編集することで、エージェントの振る舞いをカスタマイズ可能です。

## トラブルシューティング

### エラー: OPENAI_API_KEY が設定されていません
`.env` ファイルを作成し、有効なOpenAI APIキーを設定してください。

### エラー: モジュールが見つかりません
依存関係をインストールしてください:
```bash
pip install -r requirements.txt
```

### Web Search が動作しない
OpenAI Agent SDKの最新版を使用していることを確認してください:
```bash
pip install --upgrade openai-agents
```

## 既存のコードとの比較

### board_meetingとの違い
- **board_meeting**: 複数エージェントによる討論シミュレーション
- **multi_persona_hearing**: ペルソナ生成 → ヒアリング → 仮説生成の一方向フロー

### idea_generator_evaluatorとの違い
- **idea_generator_evaluator**: 生成 → 評価 → 改善の反復ループ
- **multi_persona_hearing**: 段階的に深掘りする調査フロー

## ライセンス

このプロジェクトは実験用です。

## 参考

- [OpenAI Agent SDK Documentation](https://github.com/openai/agent-sdk)
- [OpenAI Web Search API](https://developers.openai.com/api/docs/guides/tools-web-search)
- [IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md) - 質問セット評価機能の詳細実装ガイド
- [USAGE.md](USAGE.md) - 詳細な使用方法とオプション
