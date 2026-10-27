# GitHub 公开上传说明（作者本人代码）

**代码版权：** 作者已确认本项目Python脚本由本人编写，因此可以自行决定公开至GitHub，无需再额外核实其他代码作者的授权。第三方Macrostrat数据的署名与适用许可仍应遵守，详见 `SOURCE_AND_LICENSE.md`。

1. 下载并解压 `Stratigraphic_Hiatus_GitHub_Public_Ready.zip`。
2. 在 https://github.com/new 创建仓库，推荐仓库名 `stratigraphic-hiatus-reproducibility`；如果要供论文审稿人直接访问，可选 **Public**。不要勾选自动创建README、.gitignore或许可证（包内已有README和.gitignore，许可证由你自行决定）。
3. 在仓库页面点击 **Add file → Upload files**；把解压所得仓库文件夹**内部**的所有文件和子文件夹上传，保留 `src/`、`data/`、`figures/`、`scripts/` 等目录结构。不要只上传ZIP。
4. 提交后检查GitHub根目录中是否有 `PROJECT_ID.txt`、`literature_review.csv`、`README.md`、`requirements.txt`、`FILE_SHA256.csv` 和 `SOURCE_AND_LICENSE.md`。
5. 在电脑本地克隆或下载仓库，从仓库根目录运行 `python scripts/verify_repository.py`。再运行 `python scripts/restore_sadler_pairs.py` 恢复大型CSV，以及 `python src/verify_results.py` 核验论文统计结果。
6. 仓库显示为 **Public**、README能正常浏览且代码数据齐全后，将真实网址填写到论文 *Data and code availability*。

**关于 LICENSE：** 你拥有代码版权，有权自行选择是否为代码添加MIT等许可证。本次更新仅纠正了错误的“版权不明确”表述，**没有擅自添加开源许可**。没有LICENSE时，仓库可公开查看，但其他人的代码复用权限不如使用明确许可证清晰。第三方Macrostrat输入数据不应被视为受你所选择的软件许可证自动覆盖。

**上传注意：** `data/processed/sadler_pairs.csv` 原文件较大，仓库提供了无损压缩版本 `sadler_pairs.csv.gz` 及恢复脚本；不要额外上传本地恢复得到的未压缩大CSV，也不要将旧 `1(3).zip` 等其他项目文件合并进去。
