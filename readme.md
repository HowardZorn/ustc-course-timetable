这个项目可以将你的选课结果生成为ics文件供你自由使用。

打开选课界面，按`F12`进入开发者终端，点击“我的课表”后有`https://jw.ustc.edu.cn/ws/schedule-table/datum`的网络流量出现。

右击该条目，复制curl命令加上`-o datum.json`，下载选课信息到这个项目的文件夹。

运行 `python parse.py datum.json` 即可生成 `courses.ics`

## Requirements

- icalendar