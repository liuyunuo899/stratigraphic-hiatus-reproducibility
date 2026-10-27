"""Project isolation guard: never search other folders or guess input files."""
from pathlib import Path
import hashlib

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ID = 'HIATUS_STRATIGRAPHIC_REPRO_PROJECT_V1'
EXPECTED_INPUTS = {'data/raw/macrostrat_columns_na.csv': '974fed1b529b0fa65e96705c03c76d9ad0f0bc04933c5f7c851cd8c67acab188', 'data/raw/macrostrat_units_na.csv': 'ba0428fc1498573b988170e5a587d860bc021bfee2fbb6f744e6f2908a12d315', 'literature_review.csv': 'b5bdda152568c6dc4b261b3ef7f48bd37de1b57bdc665c7dacc8f8519156a7b6'}

def verify_project_inputs(quiet=True):
    marker = ROOT / "PROJECT_ID.txt"
    if not marker.is_file() or marker.read_text(encoding="utf-8").strip() != PROJECT_ID:
        raise RuntimeError("\n[数据隔离检查失败] 项目身份文件 PROJECT_ID.txt 缺失或不匹配。请使用独立解压的本项目文件夹。")
    for rel, expected_hash in EXPECTED_INPUTS.items():
        filepath = ROOT / rel
        if not filepath.is_file():
            raise FileNotFoundError(f"\n[数据隔离检查失败] 本项目指定输入缺失: {filepath}\n不会搜索电脑上的其他数据。")
        if not filepath.resolve().is_relative_to(ROOT.resolve()):
            raise RuntimeError(f"[数据隔离检查失败] 输入文件指向项目目录之外: {filepath}")
        digest = hashlib.sha256()
        with filepath.open("rb") as stream:
            for block in iter(lambda: stream.read(1024*1024), b""):
                digest.update(block)
        if digest.hexdigest() != expected_hash:
            raise RuntimeError(f"\n[数据隔离检查失败] 输入文件已变化: {filepath}\n为避免混入其他论文数据，程序已停止。请还原原始文件或为新数据建立单独项目。")
        if not quiet:
            print(f"[通过] {filepath}")
    return True

if __name__ == "__main__":
    print(f"项目目录: {ROOT}")
    print("只检查以下三个精确指定的输入文件，不扫描C盘/D盘或其他目录：")
    verify_project_inputs(quiet=False)
    print("数据隔离检查通过：三个输入文件与锁定原始数据完全一致。")
