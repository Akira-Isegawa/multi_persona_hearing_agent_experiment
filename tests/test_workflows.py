"""ワークフローのテスト."""
import pytest
from unittest.mock import patch, AsyncMock, MagicMock
import asyncio

from workflows import (
    run_multi_persona_hearing_workflow,
    run_question_evaluation_workflow,
)
from models.schemas import (
    PersonasOutput,
    InterviewQuestionsOutput,
    InterviewResponse,
    HypothesisList,
    ValidationQuestionsOutput,
)


class TestWorkflowImports:
    """ワークフロー関数のインポートテスト."""

    def test_workflow_functions_are_callable(self):
        """ワークフロー関数がコール可能."""
        assert callable(run_multi_persona_hearing_workflow)
        assert callable(run_question_evaluation_workflow)


class TestMultiPersonaHearingWorkflow:
    """複数ペルソナヒアリングワークフローのテスト."""

    def test_workflow_is_async(self):
        """ワークフロー関数が非同期関数."""
        import inspect
        assert inspect.iscoroutinefunction(run_multi_persona_hearing_workflow)

    def test_workflow_accepts_num_personas_parameter(self):
        """ワークフローが num_personas パラメータを受け入れる."""
        import inspect
        
        sig = inspect.signature(run_multi_persona_hearing_workflow)
        assert "num_personas" in sig.parameters
        assert sig.parameters["num_personas"].default == 15

    def test_workflow_accepts_verbose_parameter(self):
        """ワークフローが verbose パラメータを受け入れる."""
        import inspect
        
        sig = inspect.signature(run_multi_persona_hearing_workflow)
        assert "verbose" in sig.parameters
        assert sig.parameters["verbose"].default == True

    def test_workflow_signature_has_theme_parameter(self):
        """ワークフローが theme パラメータを持つ."""
        import inspect
        
        sig = inspect.signature(run_multi_persona_hearing_workflow)
        assert "theme" in sig.parameters


class TestQuestionEvaluationWorkflow:
    """質問評価ワークフローのテスト."""

    def test_workflow_function_exists(self):
        """質問評価ワークフロー関数が存在する."""
        assert callable(run_question_evaluation_workflow)

    def test_workflow_is_async(self):
        """質問評価ワークフロー関数が非同期関数."""
        import inspect
        assert inspect.iscoroutinefunction(run_question_evaluation_workflow)

    def test_workflow_accepts_required_parameters(self):
        """質問評価ワークフローが必要なパラメータを受け入れる."""
        import inspect
        
        sig = inspect.signature(run_question_evaluation_workflow)
        params = list(sig.parameters.keys())
        
        # 最小限の必要パラメータを持つ (theme等)
        assert len(params) > 0


class TestWorkflowIntegration:
    """ワークフロー統合テスト."""

    def test_workflow_function_documentation(self):
        """ワークフロー関数がドキュメント文字列を持つ."""
        assert run_multi_persona_hearing_workflow.__doc__ is not None
        assert len(run_multi_persona_hearing_workflow.__doc__) > 0

    def test_workflow_has_docstring_content(self):
        """ワークフロー関数のドキュメント文字列に適切な内容がある."""
        doc = run_multi_persona_hearing_workflow.__doc__
        # ワークフロー機能の説明が含まれている
        assert "Args" in doc or "theme" in doc or "実行" in doc


class TestWorkflowParameterValidation:
    """ワークフローのパラメータ検証テスト."""

    def test_num_personas_default_is_15(self):
        """デフォルトペルソナ数が15."""
        import inspect
        sig = inspect.signature(run_multi_persona_hearing_workflow)
        assert sig.parameters["num_personas"].default == 15

    def test_verbose_default_is_true(self):
        """デフォルト verbose が True."""
        import inspect
        sig = inspect.signature(run_multi_persona_hearing_workflow)
        assert sig.parameters["verbose"].default == True
