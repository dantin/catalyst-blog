+++
date = "2016-04-18T17:07:28+08:00"
title = "批量更改Java项目包名"
categories = ["Misc"]
tags = ["Scripts"]
description = "更改Java项目包名的脚步"
slug = "scripts-change-project-package-name"
+++

写了一段Shell脚本用于更改Java项目包名。

### 脚本

```bash
#!/bin/bash

old_package_name="com.projecta.work"
new_package_name="com.projectb.play"

cd ..

find . -name "*.java" | xargs sed -i -e "s/${old_package_name}/${new_package_name}/g"
find . -name "*.xml" | xargs sed -i -e "s/${old_package_name}/${new_package_name}/g"
find . -name "*.cfg" | xargs sed -i -e "s/${old_package_name}/${new_package_name}/g"
find . -name "*.html" | xargs sed -i -e "s/${old_package_name}/${new_package_name}/g"

mv src/${old_package_name//./\/} src/${new_package_name//./\/}
```
