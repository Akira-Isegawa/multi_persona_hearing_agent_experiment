# テスト実行ガイド

このプロジェクトにはPytestを使用した包括的なテストスイートが含まれています。

## テスト環境のセットアップ

まず、テスト用の依存関係をインストールしてください：

```bash
pip install -r requirements.txt
```

## テストの実行

### すべてのテストを実行

```bash
pytest
```

または

```bash
python -m pytest
```

### 特定のテストファイルを実行

```bash
pytest tests/test_schemas.py  # スキーマのテスト
pytest tests/test_formatting.py  # フォーマット関数のテスト
pytest tests/test_agents.py  # エージェント定義のテスト
pytest tests/test_workflows.py  # ワークフローのテスト
pytest tests/test_cli.py  # CLI関連のテスト
pytest tests/test_evaluation_schemas.py  # 評価スキーマのテスト
```

### 特定のテストクラスまたはテスト関数を実行

```bash
pytest tests/test_schemas.py::TestPersonaOutput  # 特定のテストクラス
pytest tests/test_schemas.py::TestPersonaOutput::test_valid_persona_creation  # 特定のテスト関数
```

### 詳細な出力を表示する

```bash
pytest -v  # 詳細情報を表示
pytest -vv  # より詳細な情報を表示
```

### テストカバレッジレポートを生成

```bash
pytest --cov=. --cov-report=html
```

これにより、`htmlcov/index.html` にカバレッジレポートが生成されます。ブラウザで開くと、各ファイルのカバレッジ詳細を確認できます。

```bash
# または python -m pytest 経由で実行
python -m pytest --cov=. --cov-report=html
```

### 特定のマーカー付きテストを実行

```bash
pytest -m "unit"  # ユニットテストのみ
pytest -m "asyncio"  # asyncioテストのみ
```

## テスト構成

テストは以下のファイルに分類されています：

### `tests/conftest.py`
- pytest フィクスチャの定義
- テストで使用するサンプルデータの作成

### `tests/test_schemas.py`
- Pydantic スキーマのバリデーション
- データモデルの整合性

### `tests/test_formatting.py`
- Markdown フォーマット関数のテスト
- 出力フォーマットの検証

### `tests/test_agents.py`
- エージェント定義のテスト
- エージェント機能の確認

### `tests/test_workflows.py`
- ワークフローの基本機能テスト
- 非同期処理のテスト

### `tests/test_cli.py`
- CLI引数パースのテスト
- ファイルI/O操作のテスト

### `tests/test_evaluation_schemas.py`
- 評価用スキーマのテスト
- レポート生成の検証

## テストのベストプラクティス

### 新しいテストを追加する際

1. 適切なテストファイルでテストを追加します
2. テストクラスにグループ化します
3. わかりやすいテスト名を使用します
4. 必要に応じて conftest.py にフィクスチャを追加します

### テスト例

```python
import pytest
from models.schemas import PersonaOutput

class TestPersonaOutput:
    """PersonaOutputスキーマのテスト."""
    
    def test_valid_creation(self):
        """正常な作成を検証."""
        persona = PersonaOutput(
            name="太郎",
            age=30,
            occupation="エンジニア",
            background="大手企業に勤務",
            needs=["効率的なツール"],
            behaviors=["毎日コーディング"],
            pain_points=["コミュニケーションオーバーヘッド"],
        )
        assert persona.name == "太郎"
        assert persona.age == 30
```

## トラブルシューティング

### OpenAI APIが利用できない場合

ワークフローテストの一部は OpenAI API を使用する場合があります。この場合、テストは自動的にスキップされます。

### 非同期テストで問題が発生する場合

`pytest-asyncio` がインストールされていることを確認してください：

```bash
pip install pytest-asyncio>=0.21.0
```

### ImportError が発生する場合

プロジェクトディレクトリからテストを実行しており、conftest.py が正しく設定されていることを確認してください：

```bash
cd /Users/akiraisegawa/Dev/multi_persona_hearing_agent_experiment
pytest
```

## 継続的統合（CI）への統合

GitHub Actions などの CI システムに統合する場合の例：

```yaml
name: Run Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.10'
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    - name: Run tests
      run: |
        pytest --cov=. --cov-report=xml
    - name: Upload coverage
      uses: codecov/codecov-action@v2
```

## 参考リンク

- [Pytest ドキュメント](https://docs.pytest.org/)
- [Pydantic ドキュメント](https://docs.pydantic.dev/)
- [pytest-asyncio](https://github.com/pytest-dev/pytest-asyncio)
