# Postage
个人化疫情地图，有空就做做吧
概述：
根据政府网站信息，爬取确诊大厦的经纬度。然后同时定位到自己的位置，进而测算出自己距离感染源的距离，并根据到感染源的距离进行预警
同时获取距离用户附近的检测点和疫苗接种点的位置，进而规划出前往自己就近且安全的检测点或疫苗接种点

定位原理：
目前只做到了定位自己距离感染源的位置
通过爬取确诊大厦的位置名称，运用MapQuest的API去爬取对应的经纬度位置。通过用户输入的街道信息，进而定位到用户的位置，然后获得距离信息

缺陷：
需要用户手动输入街道名称和街道号才能较为准确定位用户位置。暂时无法自动定位

PS：各位改了代码记得上传更新一下
