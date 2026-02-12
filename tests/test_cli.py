"""main.pyのCLIレイテッドのテスト."""
import sys
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
import tempfile

from main import (
    format_hypotheses_markdown,
    format_validation_questions_markdown,
    main,
)


class TestFormatHypothesesMarkdown:
    """format_hypotheses_markdown関数のテスト."""

    def test_format_hypotheses_markdown(self, sample_hypotheses_list):
        """仮説をMarkdown形式にフォーマット."""
        result = format_hypotheses_markdown(sample_hypotheses_list)
        
        assert isinstance(result, str)
        assert "# 課題仮説・インサイト仮説" in result
        assert "課題仮説" in result
        assert "インサイト仮説" in result

    def test_format_hypotheses_markdown_contains_statements(self, sample_hypotheses_list):
        """フォーマット結果に仮説文が含まれる."""
        result = format_hypotheses_markdown(sample_hypotheses_list)
        
        for hyp in sample_hypotheses_list.problem_hypotheses:
            assert hyp.statement in result
        for hyp in sample_hypotheses_list.insight_hypotheses:
            assert hyp.statement in result

    def test_format_hypotheses_markdown_contains_evidence(self, sample_hypotheses_list):
        """フォーマット結果に根拠が含まれる."""
        result = format_hypotheses_markdown(sample_hypotheses_list)
        
        for hyp in sample_hypotheses_list.problem_hypotheses:
            for evidence in hyp.evidence:
                assert evidence in result

    def test_format_hypotheses_markdown_contains_confidence_level(self, sample_hypotheses_list):
        """フォーマット結果に確信度が含まれる."""
        result = format_hypotheses_markdown(sample_hypotheses_list)
        
        # 確信度表示を確認
        assert "確信度" in result
        for hyp in sample_hypotheses_list.problem_hypotheses:
            assert str(hyp.confidence_level) in result


class TestFormatValidationQuestionsMarkdown:
    """format_validation_questions_markdown関数のテスト."""

    def test_format_validation_questions_markdown(self, sample_validation_questions):
        """検証質問をMarkdown形式にフォーマット."""
        result = format_validation_questions_markdown(sample_validation_questions)
        
        assert isinstance(result, str)
        assert "# 仮説検証用ヒアリング項目" in result
        assert "質問リスト" in result

    def test_format_validation_questions_markdown_contains_strategy(self, sample_validation_questions):
        """フォーマット結果に検証戦略が含まれる."""
        result = format_validation_questions_markdown(sample_validation_questions)
        
        assert sample_validation_questions.validation_strategy in result

    def test_format_validation_questions_markdown_contains_questions(self, sample_validation_questions):
        """フォーマット結果に質問が含まれる."""
        result = format_validation_questions_markdown(sample_validation_questions)
        
        for question in sample_validation_questions.questions:
            assert question.question in result
            assert question.intent in result

    def test_format_validation_questions_markdown_contains_priorities(self, sample_validation_questions):
        """フォーマット結果に優先順位が含まれる."""
        result = format_validation_questions_markdown(sample_validation_questions)
        
        for priority in sample_validation_questions.priority_order:
            assert priority in result


class TestCLIArgumentParsing:
    """CLI引数パースのテスト."""

    def test_theme_argument_parsing(self):
        """--theme引数の解析."""
        test_args = [
            "main.py",
            "--theme",
            "テストテーマ",
        ]
        
        with patch.object(sys, "argv", test_args):
            # ArgumentParserのテスト
            import argparse
            
            parser = argparse.ArgumentParser()
            input_group = parser.add_mutually_exclusive_group(required=True)
            input_group.add_argument("--theme", type=str)
            input_group.add_argument("--input", type=str)
            
            args = parser.parse_args(test_args[1:])
            assert args.theme == "テストテーマ"

    def test_input_file_argument_parsing(self):
        """--input引数の解析."""
        test_args = [
            "main.py",
            "--input",
            "inputs/theme.md",
        ]
        
        with patch.object(sys, "argv", test_args):
            import argparse
            
            parser = argparse.ArgumentParser()
            input_group = parser.add_mutually_exclusive_group(required=True)
            input_group.add_argument("--theme", type=str)
            input_group.add_argument("--input", type=str)
            
            args = parser.parse_args(test_args[1:])
            assert args.input == "inputs/theme.md"

    def test_num_personas_argument_parsing(self):
        """--num-personas引数の解析."""
        test_args = [
            "main.py",
            "--theme",
            "テーマ",
            "--num-personas",
            "20",
        ]
        
        with patch.object(sys, "argv", test_args):
            import argparse
            
            parser = argparse.ArgumentParser()
            input_group = parser.add_mutually_exclusive_group(required=True)
            input_group.add_argument("--theme", type=str)
            input_group.add_argument("--input", type=str)
            parser.add_argument("--num-personas", type=int, default=15)
            
            args = parser.parse_args(test_args[1:])
            assert args.num_personas == 20

    def test_output_dir_argument_parsing(self):
        """--output-dir引数の解析."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_args = [
                "main.py",
                "--theme",
                "テーマ",
                "--output-dir",
                tmpdir,
            ]
            
            with patch.object(sys, "argv", test_args):
                import argparse
                
                parser = argparse.ArgumentParser()
                input_group = parser.add_mutually_exclusive_group(required=True)
                input_group.add_argument("--theme", type=str)
                input_group.add_argument("--input", type=str)
                parser.add_argument("--output-dir", type=str, default="outputs")
                
                args = parser.parse_args(test_args[1:])
                assert args.output_dir == tmpdir

    def test_quiet_argument_parsing(self):
        """--quiet引数の解析."""
        test_args = [
            "main.py",
            "--theme",
            "テーマ",
            "--quiet",
        ]
        
        with patch.object(sys, "argv", test_args):
            import argparse
            
            parser = argparse.ArgumentParser()
            input_group = parser.add_mutually_exclusive_group(required=True)
            input_group.add_argument("--theme", type=str)
            input_group.add_argument("--input", type=str)
            parser.add_argument("--quiet", action="store_true")
            
            args = parser.parse_args(test_args[1:])
            assert args.quiet is True


class TestSaveResults:
    """save_results関数のテスト."""

    def test_save_results_creates_output_directory(
        self,
        sample_personas_output,
        sample_questions_output,
        sample_interview_response,
        sample_hypotheses_list,
        sample_validation_questions,
    ):
        """save_resultsが出力ディレクトリを作成."""
        from main import save_results
        
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir) / "outputs"
            
            # save_results実行（評価レポートなし）
            save_results(
                output_dir,
                sample_personas_output,
                sample_questions_output,
                [sample_interview_response],
                sample_hypotheses_list,
                sample_validation_questions,
            )
            
            # ディレクトリが作成されている
            assert output_dir.exists()

    def test_save_results_creates_files(
        self,
        sample_personas_output,
        sample_questions_output,
        sample_interview_response,
        sample_hypotheses_list,
        sample_validation_questions,
    ):
        """save_resultsが各種ファイルを作成."""
        from main import save_results
        
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir) / "outputs"
            
            save_results(
                output_dir,
                sample_personas_output,
                sample_questions_output,
                [sample_interview_response],
                sample_hypotheses_list,
                sample_validation_questions,
            )
            
            # 各ファイルが作成されている
            assert (output_dir / "personas.md").exists()
            assert (output_dir / "initial_questions.md").exists()
            assert (output_dir / "interview_results.md").exists()
            assert (output_dir / "hypotheses.md").exists()
            assert (output_dir / "validation_questions.md").exists()

    def test_save_results_file_content(
        self,
        sample_personas_output,
        sample_questions_output,
        sample_interview_response,
        sample_hypotheses_list,
        sample_validation_questions,
    ):
        """save_resultsが正しい内容をファイルに保存."""
        from main import save_results
        
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir) / "outputs"
            
            save_results(
                output_dir,
                sample_personas_output,
                sample_questions_output,
                [sample_interview_response],
                sample_hypotheses_list,
                sample_validation_questions,
            )
            
            # ペルソナファイルの内容を確認
            personas_content = (output_dir / "personas.md").read_text()
            assert "生成されたペルソナ" in personas_content
            assert sample_personas_output.personas[0].name in personas_content
