import os
import PyInstaller.__main__

package_name = "Badminton"  # 你期望生成的exe文件的名字
py_script = "App.py"  # 你要打包的python脚本的名字
json_file = "config.json"  # 你要一起打包的json文件的名字

# 生成.spec文件并打包
PyInstaller.__main__.run([
    '--name=%s' % package_name,
    '--onefile',  # 单文件exe
    '--add-data=%s;.' % json_file,  # 将json文件添加到打包目录
    '--clean',  # 清理打包过程的临时文件
    os.path.join(os.getcwd(), py_script),
])

print('打包完成。')

