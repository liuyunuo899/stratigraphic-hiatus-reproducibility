# 地层缺失论文代码和数据：中文说明

这是基于本次上传的 `1(3).zip` **实际代码、CSV和ESR英文稿**整理的GitHub仓库。不修改 `src/` 中任何科学计算脚本，也不修改原始或模拟数据的数值。

## 为什么补文件

本次压缩包缺少 `PROJECT_ID.txt`、`literature_review.csv`、`requirements.txt`、README等文件。`project_guard.py` 强制要求前两者且会核对SHA-256；缺失时所有主要脚本都不能启动。文献表由此前同一项目、与本次代码内SHA-256完全一致的版本恢复，没有重新编造55条文献。身份文件按原代码中的固定字符串生成。

## 运行步骤（Windows / Anaconda Prompt）

将下载的ZIP解压到英文目录（非必须，但可避免部分Windows路径兼容性问题），进入解压得到的文件夹，在根目录执行：

```bat
python -m pip install -r requirements.txt
python scripts/verify_repository.py
python scripts/restore_sadler_pairs.py
python src/project_guard.py
python src/verify_results.py
```

`sadler_pairs.csv` 约40 MB，已无损压缩为 `data/processed/sadler_pairs.csv.gz` 方便网页上传。**必须先运行恢复脚本，才能运行原 `analysis.py`、`verify_results.py`。** 恢复脚本对照原始SHA-256，并且不会覆盖内容不同的本地文件。

如果要从固定数据重新计算：

```bat
python src/data_processing.py
python src/analysis.py
python src/simulation.py
python src/inversion.py
python src/verify_results.py
```

再运行 `src/figure_01.py` 至 `src/figure_10.py` 即可按原始十图脚本绘图。**不需要重新下载Macrostrat；不要运行 `data_fetch.py` 来代替固定快照。**

## 图号说明

投稿Word正文为Figure 1–9，补充文件只有Supplementary Fig. S1；代码仍使用 `figure_01`–`figure_10` 原编号。代码中的Figure 2为补充图，原Figure 3–10顺次对应投稿Figure 2–9。详细对应关系见 `FIGURE_MAP.md`。

## 上传GitHub

1. **你已确认本项目Python代码由你本人编写，可以选择公开（Public）仓库。** 注意：Macrostrat原始数据仍需按其数据提供方的许可要求保留署名和来源。
2. GitHub上创建新仓库，不要自动勾选生成README。
3. 解压本ZIP，把里面仓库文件夹**内部**所有文件、子文件夹一起上传；不要只上传ZIP。
4. GitHub网页单文件上限较低，所以大CSV以gzip形式放入。
5. 检查GitHub页面中的README、`src/`、`data/`、`literature_review.csv`、`scripts/` 是否齐全。
6. 上传成功后检查全部文件，若仓库为 **Public**，即可将其真实地址填入论文的 *Data and code availability*（未上传成功前不要提前声称已公开）。

`ESR_Manuscript.docx`和`ESR_Supplement.docx`是排版稿件，**未放进公开代码仓库**；仅提取了稿件内的投稿PNG图，放在 `figures/submission/`，以对应正文和补充材料。原始Word仍保留在你自己的压缩包中。

## 关于开源许可证

代码版权归你所有，是否添加 MIT 等开源许可证由你决定。当前包**未自动增加 LICENSE**：GitHub 仓库设为 Public 只代表公众可以访问，并不等于已明确授予他人修改或再分发代码的许可。如打算授权科研同行复用，可在 GitHub 仓库中另行选择 MIT 等许可证；注意该许可证不能自动覆盖 Macrostrat 第三方原始数据。
