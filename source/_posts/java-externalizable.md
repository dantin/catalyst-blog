---
title: Java中的外部序列化
date: 2016-03-17 17:17:20
categories: 工程
tags: Java
toc: true
---

Externalizable是Serializable的子接口，在Java中，通过Externlizable，也能实现序列化。

### 接口

Externlizable的源代码如下:

```java
public interface Externalizable extends java.io.Serializable {

    void writeExternal(ObjectOutput out) throws IOException;

    void readExternal(ObjectInput in) throws IOException, ClassNotFoundException;
}
```

Exterinable的是Serializable的一个扩展，它继承了java的序列化接口，并增加了两个方法。

1. writeExternal()，序列化方法，该方法里义了哪些属性可以序列化，哪些不可以序列化，所以，对象在这里规定了能被序列化的内容，不能序列化的不处理；
2. readExternal()，反序列化方法，根据序列顺序挨个读取进行反序列，并自动封装成对象返回，最终完成反序列化；

### 使用

为了更好的理解相关内容，请看下面的例子。

```java
class Person implements Externalizable {
    private static final long serialVersionUID = 1L;
    String userName;
    String password;
    String age;
    
    public Person(String userName, String password, String age) {
        super();
        this.userName = userName;
        this.password = password;
        this.age = age;
    }
     
    public Person() {
        super();
    }
 
    public String getAge() {
        return age;
    }
    public void setAge(String age) {
        this.age = age;
    }
    public String getUserName() {
        return userName;
    }
    public void setUserName(String userName) {
        this.userName = userName;
    }
    public String getPassword() {
        return password;
    }
    public void setPassword(String password) {
        this.password = password;
    }
     
    /**
     * 序列化操作的扩展类
     */
    @Override
    public void writeExternal(ObjectOutput out) throws IOException {
        //增加一个新的对象
        Date date=new Date();
        out.writeObject(userName);
        out.writeObject(password);
        out.writeObject(date);
    }
     
    /**
     * 反序列化的扩展类
     */
    @Override
    public void readExternal(ObjectInput in) throws IOException,
            ClassNotFoundException {
        // 注意这里的接受顺序是有限制的哦，否则的话会出错的
        // 例如上面先write的是A对象的话，那么下面先接受的也一定是A对象...
        userName=(String) in.readObject();
        password=(String) in.readObject();
        SimpleDateFormat sdf=new SimpleDateFormat("yyyy-MM-dd");
        Date date=(Date)in.readObject();       
        System.out.println("反序列化后的日期为:"+sdf.format(date));
         
    }
    @Override
    public String toString() {
        //注意这里的年龄是不会被序列化的，所以在反序列化的时候是读取不到数据的
        return "用户名:"+userName+"密 码:"+password+"年龄:"+age;
    }
}
```

序列化和反序列化的相关操作类。

```java
class Operate {

    public void serializable(Person person) throws FileNotFoundException, IOException{
        ObjectOutputStream outputStream=new ObjectOutputStream(new FileOutputStream("a.txt"));
        outputStream.writeObject(person);      
    }

    public Person deSerializable() throws FileNotFoundException, IOException, ClassNotFoundException{
        ObjectInputStream ois=new ObjectInputStream(new FileInputStream("a.txt"));
        return (Person) ois.readObject();
    }
}
```

测试实体主类

```java
public class Test {
    public static void main(String[] args) throws FileNotFoundException, IOException, ClassNotFoundException {
       Operate operate=new Operate();
       Person person=new Person("姓名","123456","20");
       System.out.println("为序列化之前的相关数据如下:\n"+person.toString());
       operate.serializable(person);
       Person newPerson=operate.deSerializable();
       System.out.println("-------------------------------------------------------");
       System.out.println("序列化之后的相关数据如下:\n"+newPerson.toString());
    }
}
```

Person类实现了Externalizable 接口，在writeExternal()方法里定义了哪些属性可以序列化，哪些不可以序列化，所以，对象在此方法中把规定能被序列化的属性序列化为文件，不能序列化的不处理，然后在反序列的时候自动调用readExternal()方法，根据序列顺序挨个读取进行反序列，并自动封装成对象返回，最终完成反序列.

摘自：
* [CNBlogs](http://www.cnblogs.com/xiohao/p/4234184.html)
