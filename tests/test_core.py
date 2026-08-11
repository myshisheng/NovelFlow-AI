import tempfile,unittest
from pathlib import Path
from novelflow.canon import add_fact,add_foreshadow,report,resolve_foreshadow
from novelflow.chapters import approve,set_chapter,set_chapter_summary
from novelflow.context import build_context
from novelflow.exporters import export_book
from novelflow.storage import complete_task,init_project,list_tasks
from novelflow.workflow import bootstrap,next_task

class T(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.root=init_project(Path(self.tmp.name)/"book",idea="每天暂停时间十秒",platform="番茄",genre="都市异能",target_words=1500000,chapters=600)
    def tearDown(self): self.tmp.cleanup()
    def test_bootstrap(self):
        self.assertEqual(len(bootstrap(self.root)),4); self.assertEqual(len(bootstrap(self.root)),0); t=next_task(self.root); self.assertEqual(t["status"],"in_progress"); complete_task(self.root,t["id"],"完成"); self.assertEqual(sum(x["status"]=="done" for x in list_tasks(self.root)),1)
    def test_approval(self):
        set_chapter(self.root,1,"# 第1章\n正文")
        with self.assertRaises(ValueError): approve(self.root,1)
        set_chapter_summary(self.root,1,"主角获得能力。"); self.assertEqual(approve(self.root,1)["approved_chapters"],1)
    def test_canon_context(self):
        add_fact(self.root,"能力每天最多10秒"); fs=add_foreshadow(self.root,"怀表来源",3,10); set_chapter_summary(self.root,1,"获得怀表"); ctx=build_context(self.root,2,5); self.assertIn("能力每天最多10秒",ctx); self.assertIn("获得怀表",ctx); resolve_foreshadow(self.root,fs["id"],9,"揭示"); self.assertEqual(report(self.root)["unresolved_foreshadowing"],0)
    def test_export(self):
        set_chapter(self.root,1,"# 第一章\n你好，世界。"); set_chapter_summary(self.root,1,"开场")
        for f in ("txt","md","html"): self.assertTrue(export_book(self.root,f).exists())
if __name__=="__main__": unittest.main()
