参考：[【制作数据集时，用python脚本对标注信息进行数据清洗和可视化】](https://blog.csdn.net/Kefenggewu_/article/details/112383750)

所有操作在`tools`文件夹下进行：
1. check_xml_name.py：检查所标注的xml文件中是否有命名不合规范的存在
2. check_defect_xml.py：对比数据源图（jpg）与所保存的标注的xml文件，打印缺失的xml图片序号
3. del_no_xml_img.py删除没有对应xml文件的jpg文件
4. export_xml_info_to_excel.py：将标注的所有xml文件信息写入一个excel表格，后期数据分析使用
5. produce_report.py：数据分析，查看xml文件统计信息，生成网页数据报告

rewrite_xml_name.py：重新命名已标注好的xml文件中的label名称（beizi->cup）
find_error_xml.py：发现xml标注文件的明显错误
get_all_labels.py：得到所有xml标注的数据标签
LabelToolForDetection：目标检测标注工具
SimpleLabeltool：目标检测标注工具