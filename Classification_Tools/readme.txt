打包：pyinstaller -F Classification_Tools.py
会生成Classification_Tools.exe

原始待分类图片全部放在data_all文件夹内，双击Classification_Tools.exe启动程序，因为我是4个类别所以程序会自动创建0，1，2，3文件夹和unconfirmed文件夹，此时我们只需使用按键0，1，2，3即可将当前图片存放进相应的文件夹内，按右键可跳过当前图片进行下一张图片，如果前一张分错了则按左键，会返回前一张图片然后重新进行分类，完成图片分类。如果遇到不确定或者不需要的图片则按d键图片会放进unconfirmed文件夹内