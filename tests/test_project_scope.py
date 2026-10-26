import importlib.util
from pathlib import Path
import tempfile
import unittest


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "check_project_scope.py"
SPEC = importlib.util.spec_from_file_location("check_project_scope", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class ProjectScopeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.workspace = Path(self.temp.name)
        self.project_a = self.workspace / "project-a"
        self.project_b = self.workspace / "project-b"
        self.project_a.mkdir()
        self.project_b.mkdir()
        self.anchor = self.project_a / "src.txt"
        self.anchor.write_text("project A", encoding="utf-8")

    def test_current_project_note_is_allowed(self):
        result = MODULE.check_scope(
            str(self.project_a), "docs/PROJECT_CONTEXT.md", str(self.anchor)
        )
        self.assertEqual(result["relative_target"], str(Path("docs/PROJECT_CONTEXT.md")))

    def test_sibling_project_is_rejected(self):
        with self.assertRaises(MODULE.ScopeError):
            MODULE.check_scope(
                str(self.project_a), str(self.project_b / "PROJECT_CONTEXT.md"), str(self.anchor)
            )

    def test_nested_git_project_is_rejected(self):
        nested = self.project_a / "vendor"
        nested.mkdir()
        (nested / ".git").mkdir()
        with self.assertRaises(MODULE.ScopeError):
            MODULE.check_scope(str(self.project_a), "vendor/AGENTS.md", str(self.anchor))

    def test_anchor_in_other_project_is_rejected(self):
        other_anchor = self.project_b / "src.txt"
        other_anchor.write_text("project B", encoding="utf-8")
        with self.assertRaises(MODULE.ScopeError):
            MODULE.check_scope(str(self.project_a), "README.md", str(other_anchor))

    def test_symlink_escape_is_rejected_when_supported(self):
        link = self.project_a / "linked"
        try:
            link.symlink_to(self.project_b, target_is_directory=True)
        except (OSError, NotImplementedError) as exc:
            self.skipTest(f"directory symlinks unavailable: {exc}")
        with self.assertRaises(MODULE.ScopeError):
            MODULE.check_scope(str(self.project_a), "linked/PROJECT_CONTEXT.md")


if __name__ == "__main__":
    unittest.main()
