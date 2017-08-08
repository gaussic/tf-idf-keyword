# 基于TD-IDF的中文关键词提取

## IDF(逆文档频率)生成

用法：

```bash
$ python gen_idf.py -i <inputdir> -o <outputfile>
```

- `-i <inputdir>`   ： 语料库目录，程序会扫描目录下的所有文件
- `-o <outputfile>` ： 保存idf到指定文件

## TF-IDF关键词提取

用法：

```bash
$ python tfidf.py -i <idffile> -d <document> -t <topK>
```
- `-i <idffile>`  ： idf文件路径
- `-d <document>` ： 所需处理文档路径
- `-t <topK>`     ： 返回topK结果


