## 项目设计

### 需求实现

**列表页**：

- `Add User` button
- 表格展示字段，id, name, gender, edit（button）
- 分页展示

**编辑弹框**：

- 标题：Add User / Edit User
- 字段: name（文本框），gender（下拉框）
- 按钮：Confirm / Cancel

### 前端技术栈

创建前端目录：`demo_front`

Vue3+Vite+Tailwind CSS+Axios

**api域名**：`https://api.localhost.com`

### 后端技术栈

创建后端目录：`demo_back`

Python3+Flask+SQLAlchemy ORM+Mysql

**注意** 在 `demo_back` 目录下创建并使用python3的虚拟环境，并安装requirements.txt中的依赖

### 数据库连接

```python
from sqlalchemy import create_engine

engine = create_engine('mysql+pymysql://root:t7d4j8m9@dbconn.sealoshzh.site:36452/demo_project_preview')
```
