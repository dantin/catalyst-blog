title: Hadoop开发调试环境配置
date: 2016-03-14 16:29:24
categories: 工程
tags: [Hadoop, Java]
toc: true
---

学习Hadoop的过程中经常需要编译和调试Java代码，为方便起见，在Mac OSX环境中利用IntelliJ IDEA搭建了Hadoop的开发环境。只要在IDEA环境中导入Hadoop的核心包，就可以在IDEA环境下编译MapReduce程序，配置生成相应的jar包。通过将该jar包导入到本地服务器的Hadoop集群，就可以运行相应的MapReduce程序。

这里以官方的WordCount程序作为例子。

### Maven项目

首先在IDEA新建一个Maven项目。

`pom.xml`如下：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>com.cosmos</groupId>
    <artifactId>hadoop-samples</artifactId>
    <version>1.0-SNAPSHOT</version>

    <description>Hadoop的示例程序</description>

    <dependencies>
        <!-- 开发一个普通的Hadoop项目,需要hadoop-common依赖 -->
        <dependency>
            <groupId>org.apache.hadoop</groupId>
            <artifactId>hadoop-common</artifactId>
            <version>2.7.2</version>
        </dependency>
        <!-- hadoop-2 does not have hadoop-core project anymore. -->
        <!-- replace hadoop-core with hadoop-common or put hadoop-core to hadoop-1 profile -->
        <!-- https://github.com/cloudera/hue/issues/104 -->
        <!--
            <dependency>
                <groupId>org.apache.hadoop</groupId>
                <artifactId>hadoop-core</artifactId>
                <version>1.2.1</version>
            </dependency>
        -->
        <!-- 如果需要读取HDFS上的文件内容,需要hadoop-hdfs和hadoop-client依赖 -->
        <dependency>
            <groupId>org.apache.hadoop</groupId>
            <artifactId>hadoop-hdfs</artifactId>
            <version>2.7.2</version>
        </dependency>
        <dependency>
            <groupId>org.apache.hadoop</groupId>
            <artifactId>hadoop-client</artifactId>
            <version>2.7.2</version>
        </dependency>
        <!-- 如果需要读取HBase的数据,需要加上hbase-client依赖 -->

    </dependencies>

</project>
```

这里使用的Hadoop测试集群版本是2.7.2，具体的`pom.xml`配置需要根据集群的具体发行版本修改。如果版本不一致将会出现hadoop集群无法正常运行MapReduce程序的情况。

开发一个普通的Hadoop项目，一般需要`hadoop-common`依赖；如果需要读取HDFS上的文件内容，则需要`hadoop-hdfs`和`hadoop-client`另外两组依赖；如果需要读取HBase的数据，则需要再加入`hbase-client`。

### WordCount代码

使用Hadoop自带的源码：

```java
import java.io.IOException;
import java.util.StringTokenizer;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class WordCount {

    public static class TokenizerMapper extends Mapper<Object, Text, Text, IntWritable> {

        private final static IntWritable one = new IntWritable(1);
        private Text word = new Text();

        public void map(Object key, Text value, Context context)
                throws IOException, InterruptedException {
            StringTokenizer itr = new StringTokenizer(value.toString());
            while (itr.hasMoreTokens()) {
                word.set(itr.nextToken());
                context.write(word, one);
            }
        }
    }

    public static class IntSumReducer extends Reducer<Text, IntWritable, Text, IntWritable> {
        private IntWritable result = new IntWritable();

        public void reduce(Text key, Iterable<IntWritable> values, Context context)
                throws IOException, InterruptedException {
            int sum = 0;
            for (IntWritable val : values) {
                sum += val.get();
            }
            result.set(sum);
            context.write(key, result);
        }
    }

    public static void main(String[] args) throws Exception {
        Configuration conf = new Configuration();

        Job job = Job.getInstance(conf, "word count");
        job.setJarByClass(WordCount.class);

        job.setMapperClass(TokenizerMapper.class);
        job.setCombinerClass(IntSumReducer.class);
        job.setReducerClass(IntSumReducer.class);
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(IntWritable.class);

        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));

        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}
```

### 生成jar包

生成jar包的过程也比较简单， 

1. 选择菜单File->Project Structure，弹出Project Structure的设置对话框。
2. 选择左边的Artifacts后点击上方的“+”按钮
3. 在弹出的框中选择jar->Empty
4. 在“Output Layout”中，选择“Module Output”要启动的类，并勾选构件时重新编译打包（Build on make）
5. 应用之后，对话框消失。在IDEA选择菜单Build->Build Artifacts,选择Build或者Rebuild后即可生成，生成的jar文件位于工程项目目录的out/artifacts下。

### 运行jar包

将生成的wordcount.jar传送到hadoop集群的Name node节点上。 处于测试目的，简单写了一个测试数据文本wctest.txt

```bash
this is hadoop test string
hadoop hadoop
test test
string string string
```

将该测试文本传到HDFS

```bash
hdfs dfs -mkdir wc_test_input
hdfs dfs -put wctest.txt wc_test_input
```

cd 到jar包对应的目录，执行HelloHadoop jar包

```bash
hadoop jar wordcount.jar WordCount wc_test_input wc_test_output
16/03/14 15:43:56 WARN util.NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
16/03/14 15:43:57 INFO Configuration.deprecation: session.id is deprecated. Instead, use dfs.metrics.session-id
16/03/14 15:43:57 INFO jvm.JvmMetrics: Initializing JVM Metrics with processName=JobTracker, sessionId=
16/03/14 15:43:57 WARN mapreduce.JobResourceUploader: Hadoop command-line option parsing not performed. Implement the Tool interface and execute your application with ToolRunner to remedy this.
16/03/14 15:43:57 INFO input.FileInputFormat: Total input paths to process : 1
16/03/14 15:43:57 INFO mapreduce.JobSubmitter: number of splits:1
16/03/14 15:43:58 INFO mapreduce.JobSubmitter: Submitting tokens for job: job_local242506982_0001
...
16/03/14 15:43:59 INFO mapred.LocalJobRunner: Finishing task: attempt_local242506982_0001_r_000000_0
16/03/14 15:43:59 INFO mapred.LocalJobRunner: reduce task executor complete.
16/03/14 15:43:59 INFO mapreduce.Job: Job job_local242506982_0001 running in uber mode : false
16/03/14 15:43:59 INFO mapreduce.Job:  map 100% reduce 100%
16/03/14 15:43:59 INFO mapreduce.Job: Job job_local242506982_0001 completed successfully
16/03/14 15:43:59 INFO mapreduce.Job: Counters: 35
    File System Counters
        FILE: Number of bytes read=6608
        FILE: Number of bytes written=602619
        FILE: Number of read operations=0
        FILE: Number of large read operations=0
        FILE: Number of write operations=0
        HDFS: Number of bytes read=142
        HDFS: Number of bytes written=37
        HDFS: Number of read operations=13
        HDFS: Number of large read operations=0
        HDFS: Number of write operations=4
    Map-Reduce Framework
        Map input records=4
        Map output records=12
        Map output bytes=120
        Map output materialized bytes=63
        Input split bytes=137
        Combine input records=12
        Combine output records=5
        Reduce input groups=5
        Reduce shuffle bytes=63
        Reduce input records=5
        Reduce output records=5
        Spilled Records=10
        Shuffled Maps =1
        Failed Shuffles=0
        Merged Map outputs=1
        GC time elapsed (ms)=0
        Total committed heap usage (bytes)=617611264
    Shuffle Errors
        BAD_ID=0
        CONNECTION=0
        IO_ERROR=0
        WRONG_LENGTH=0
        WRONG_MAP=0
        WRONG_REDUCE=0
    File Input Format Counters
        Bytes Read=71
    File Output Format Counters
        Bytes Written=37
```

结果被输出到`wc_test_output`

```bash
hdfs dfs -ls wc_test_output
Found 2 items
-rw-r--r--   1 david supergroup          0 2016-03-14 15:43 wc_test_output/_SUCCESS
-rw-r--r--   1 david supergroup         37 2016-03-14 15:43 wc_test_output/part-r-00000
hdfs dfs -cat /user/chenbiaolong/wc_test_output/part-r-00000
hadoop  3
is      1
string  4
test    3
this    1
```

参考：

1. [IntelliJ Hadoop MapReduce的开发调试](http://my.oschina.net/zhangdengpan/blog/356641)
2. [Apache Hadoop官方MapReduce教程](https://hadoop.apache.org/docs/current/hadoop-mapreduce-client/hadoop-mapreduce-client-core/MapReduceTutorial.html)