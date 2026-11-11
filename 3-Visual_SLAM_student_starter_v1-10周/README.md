# 最后一课：视觉SLAM代码任务（学生版）

## 今天不是从零实现完整SLAM
巡检小车要从图像认识相同位置，并判断相机/地图估计是否合理。本次完成六个关键小步骤；不要求编译完整ORB-SLAM、不要求写BA优化器、不用单位步长拼出“米制轨迹”。

只编辑 student_tasks.py 的TODO函数体。读取、验证、数据、绘图、异常处理和多本质矩阵候选等由框架提供。
代码长度不是评分依据：重点是正确实现、解释输入输出，以及理解单位和边界。

## 三种材料怎样配合
| TODO | 函数 | 阅读材料 | 学生易懂版PPT | 必须解释 |
|---|---|---|---|---|
| T1 | hamming_bits | 03 匹配 | 6—8页 | 距离2不是2像素 |
| T2 | world_to_camera | 01 坐标 | 10—12页 | 变的是参考系；t不是直接抄小车位置 |
| T3 | project_pinhole | 02 投影 | 13—15页 | 深度加倍，主点偏移减半 |
| T4 | reprojection_scores | 06 误差 | 22—25页 | 残差、平方和、RMSE单位不同 |
| T5 | match_orb_descriptors | 03 匹配 | 31—33页 | 外观候选不等于几何内点 |
| T6 | recover_one_pose | 04＋05 | 33—36页 | t是变换中的单位方向，不是米数 |

按核心数学→库接口→综合运行分段完成，代码练习顺序不等于完整SLAM执行顺序。

## 课前环境
推荐已准备好的Python 3.8及以上环境。不要在课堂临时编译ROS/ORB-SLAM。
基础：python -m pip install -r requirements-core.txt
完整：python -m pip install -r requirements-full.txt
若已安装可工作的opencv-python，不要再同时安装另一个OpenCV发行包；由教师统一确认。

环境检查：
python preflight.py
python preflight.py --full

第二条失败时，T5/T6不能算通过；先修复环境。OpenCV测试SKIP不等于PASS。
基础T1—T4只依赖NumPy；Matplotlib用于可视化。第一次运行测试出现NotImplementedError是预期现象，不是安装坏了。

## 推荐工作顺序
1. 阅读题→纸上算一次→补相应TODO。
2. 每完成一个函数先运行该任务的测试。
3. T1—T4完成后运行核心实验。
4. T5/T6完成后运行匹配与运动实验。
5. 填写submission.md，解释结果与单位。

单项测试示例：
python -m unittest tests.test_core.TestT1 -v
python -m unittest tests.test_core.TestT2 -v
python -m unittest tests.test_core.TestT3 -v
python -m unittest tests.test_core.TestT4 -v
python -m unittest tests.test_opencv.TestT5 -v
python -m unittest tests.test_opencv.TestT6 -v

必做公开自测：python -m unittest discover -s tests -v
选做测试：python -m unittest tests.optional_checks -v
选做不计入默认必做测试，不影响基础100分。

## 运行实验
数学与评分：python run_lab.py --stage core --out outputs
直接检查T6：python run_lab.py --stage pose --out outputs
匹配后几何：python run_lab.py --stage matching --out outputs
全部合成实验：python run_lab.py --stage all --out outputs

outputs将包含JSON、CSV和评分图。核心实验展示四个点的多点评分；阅读材料中“13”是一个点的平方和，不能混为同一个总分。

实图拓展（先验证输入）：
python run_lab.py --stage images --image1 IMAGE1 --image2 IMAGE2 --fx FX --fy FY --cx CX --cy CY --undistorted --out outputs_real
把大写占位符替换为实际路径和像素内参。--undistorted表示你确认图片已去畸变，不是程序自动去畸变。

## 数据诚实说明
自带三套合成数据，无需联网下载：
- scoring_fixture.npz：构造的地图点和扰动观测，比较给定候选，不执行BA优化。
- pose_fixture.npz：理想针孔投影的3D点、对应像素和已知本质矩阵候选。
- matching_fixture.npz：模拟256位二进制描述子，不是从实拍图提取的ORB；用于接口与几何连接练习。
完整说明见data/MANIFEST.json。合成实验通过不能替代实拍数据或真实SLAM精度验证。

## 两级提示
先做题，再按需要查看；不要跳过解释。
T1：①逐位对齐；②把每次“不同”视为一次计数。
T2：①先想一个列向量点如何旋转；②数组按行存点，注意转置与广播。
T3：①先求横向/纵向与深度的比值；②分别乘对应焦距再加主点，返回N行2列。
T4：①先做观测减预测；②每行平方相加，再对点求和。RMSE分母是点数N，不是2N。
T5：①默认ORB为二进制指纹；②选择汉明范数、双向互选，按.distance升序返回列表。
T6：①读取OpenCV官方recoverPose接口；②同一内参、复制mask，原样返回四个输出，不人为补米制长度。

## 选做
T7：求相机2中心在相机1中的表示，理解为什么要对点变换取逆。
T8：场景与变换平移同比例缩放，比较投影不变；不能只缩放点、不缩放平移。

## 提交
- student_tasks.py（已完成的函数，不提交环境目录）；
- submission.md（每个人都要能解释）；
- 测试终端输出，包含SKIP信息；
- core_report.json、residuals.csv和评分图；
- OpenCV环境可用时再附matching_report.json与pose_report.json。
若T5/T6未完成或环境失败，明确标注，不把SKIP写成通过。
