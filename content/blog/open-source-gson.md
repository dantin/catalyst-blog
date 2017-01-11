+++
date = "2016-12-16T21:58:41+08:00"
title = "Json工具库：Gson"
categories = ["Engineering"]
tags = ["Memo", "Open Source"]
description = "本文记录Google Gson库的简单用法"
slug = "open-source-gson"
+++

Json是一种数据格式，便于数据传输、存储、交换；而Gson是Google开源的Json序列化／反序列化库。

本文简单记录Gson的常见用法。

### Json对象格式

#### 单个数据对象

```json
{
    "id": 100,
    "body": "It is my post",
    "number": 0.13,
    "created_at": "2014-05-22 19:12:38"
}
```

#### 数组对象

数组是用$[]$围起来的，内部{}围起来的就是单个的数据对象。

```json
[
    {
        "id": 100,
        "body": "It is my post1",
        "number": 0.13,
        "created_at": "2014-05-20 19:12:38"
    },
    {
        "id": 101,
        "body": "It is my post2",
        "number": 0.14,
        "created_at": "2014-05-22 19:12:38"
    }
]
```

#### 嵌套数据对象

嵌套数据是用`{}`围起来的单个数据对象，其内部又是一个数据对象。

```json
{
    "id": 100,
    "body": "It is my post",
    "number": 0.13,
    "created_at": "2014-05-22 19:12:38",
    "foo2": {
        "id": 200,
        "name": "haha"
    }
}
```

### 反序列化

#### Json字符串

在JsonReader的构造函数中传入json data，然后开始解析，判断是否还有下一个对象，如果有就开始解析对象名和对象体，直到解析完毕。

```java
@Test
public void testJsonReader() {
    String jsonData = "[{\"username\":\"name01\",\"userId\":001},{\"username\":\"name02\",\"userId\":002}]";

    JsonReader reader = new JsonReader(new StringReader(jsonData));
    // 在宽松模式下解析
    reader.setLenient(true);

    try {
        // 开始解析数组（包含一个或多个Json对象）
        reader.beginArray();
        // 如果有下一个数据就继续解析
        while (reader.hasNext()) {
            // 开始解析一个新的对象
            reader.beginObject();
            while (reader.hasNext()) {
                // 得到下一个属性名
                String tagName = reader.nextName();
                assertNotNull(tagName);
                if ("username".equals(tagName)) {
                    System.out.println(reader.nextString());
                } else if ("userId".equals(tagName)) {
                    System.out.println(reader.nextString());
                }
            }
            // 结束对象的解析
            reader.endObject();
        }
        // 结束解析当前数组
        reader.endArray();
    } catch (IOException e) {
        e.printStackTrace();
    }
}
```

#### 文件

数据是定义在本地文件系统，所以要先加载到内存中。方法是通过getAssets()得到AssetManager对象，再通过open(文件名)来获得文件流。

这里因为能确保本地的文件小于5K，所以就没做循环读取，实际中请务必用循环读取的方式。最终得到的数据存放在string中。

```java
protected InputStream getAssets(String path) throws FileNotFoundException {
    return Thread.currentThread().getContextClassLoader().getResourceAsStream(path);
}

protected String getStringFromAssets(String name) {
    String string = null;
    try {
        InputStream inputStream = getAssets(name);
        byte buf[] = new byte[5 * 1024];
        //noinspection ResultOfMethodCallIgnored
        inputStream.read(buf);
        string = new String(buf);
        string = string.trim();
    } catch (IOException e) {
        e.printStackTrace();
    }

    System.out.println("string = " + string);
    return string;
}
```

#### 类和内部类

首先，要建一个类：

```java
public class Foo1 {

    private int id;

    private String body;

    private float number;

    @SerializedName("created_at")
    private Date createdAt;

    // getter/setter
    ...
}
```

类里面的成员变量名必须跟Json字段匹配。

如果Json是嵌套定义的，则可定义内部类。

```json
{
  "id": 100,
  "body": "It is my post",
  "number": 0.13,
  "created_at": "2014-05-22 19:12:38",
  "childFoo": {
    "id": 200,
    "name": "jack"
  }
}
```

上述Json对应的类如下：

```java
public class Foo2 {
    private int id;
    private String body;
    private float number;
    @SerializedName("created_at")
    private Date createAt;
    private ChildFoo childFoo;

    // getter/setter
    ...

    public class ChildFoo {
        private int id;
        private String name;

        // getter/setter
        ...
    }
}
```

其中`@SerializedName`注解可以重命名Field。

通过`fromJson()`方法可以很方便地完成反序列化。

```java
@Test
public void testGson() {
    Gson gson = new Gson();
    Foo1 foo = gson.fromJson(getStringFromAssets("assets/json1.json"), Foo1.class);
    System.out.println(foo);
    assertNotNull(foo);
}
```

#### 数组

反序列化数组也很简单。

```java
@Test
public void testDeserializeToArray() {
    Foo1[] foos = new GsonBuilder().setDateFormat("yyyy-MM-dd HH:mm:ss").create()
            .fromJson(getStringFromAssets("assets/json_array.json"), Foo1[].class);
    System.out.println(Arrays.toString(foos));
    assertNotNull(foos);
    assertEquals(2, foos.length);
}
```

#### 集合类

这里需要指定类型`Type`。

```java
@Test
public void testDeserializeToList() {
    Type listType = new TypeToken<ArrayList<Foo1>>() {
    }.getType();

    ArrayList<Foo1> foos = new GsonBuilder().setDateFormat("yyyy-MM-dd HH:mm:ss").create()
            .fromJson(getStringFromAssets("assets/json_array.json"), listType);
    System.out.println(foos);
    assertNotNull(foos);
    assertEquals(2, foos.size());
}
```

#### 特殊字段处理

如果碰上日期，需要另外设置

```java
@Test
public void testGsonBuilder() {
    GsonBuilder gsonBuilder = new GsonBuilder();
    // 设置日期的格式，遇到这个格式的数据转为Date对象
    gsonBuilder.setDateFormat("yyyy-MM-dd HH:mm:ss");
    Gson gson = gsonBuilder.create();

    Foo1 foo = gson.fromJson(getStringFromAssets("assets/json2.json"), Foo1.class);
    System.out.println(foo);
    assertNotNull(foo);
}
```

### 实验数据

简单对象，如json1.json

```json
{
  "id": 100,
  "body": "It is my post",
  "number": 0.13
}
```

特殊格式内容，如：json2.json

```json
{
  "id": 100,
  "body": "It is my post",
  "number": 0.13,
  "created_at": "2014-05-22 19:12:38"
}
```

嵌套对象，如：json3.json

```json
{
  "id": 100,
  "body": "It is my post",
  "number": 0.13,
  "created_at": "2014-05-22 19:12:38",
  "childFoo": {
    "id": 200,
    "name": "jack"
  }
}
```

数组对象，如：json_array.json

```json
[
  {
    "id": 100,
    "body": "It is my post1",
    "number": 0.13,
    "created_at": "2014-05-20 19:12:38"
  },
  {
    "id": 101,
    "body": "It is my post2",
    "number": 0.14,
    "created_at": "2014-05-22 19:12:38"
  }
]
```