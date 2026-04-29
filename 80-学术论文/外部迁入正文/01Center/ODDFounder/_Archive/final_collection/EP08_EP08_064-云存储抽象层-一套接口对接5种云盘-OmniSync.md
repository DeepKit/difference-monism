# 云存储抽象层：一套接口对接5种云盘

> **作者**: Fuyi ( ODDFounder  fuyi.it@live.cn )
> **日期**: 2026-01-11
> **标签**: 存储抽象, 适配器模式, S3, WebDAV, OmniSync

---

## 摘要

用户的数据可能在 AWS S3，可能在阿里云 OSS，也可能在自家 NAS 的 WebDAV 上。**OmniSync** 为了支持多云备份，设计了一个 **ICloudStorage 抽象层**。通过适配器模式，应用层只需要调用 `Upload`, `Download`, `List`，底层的 S3 签名、WebDAV XML 解析等复杂细节统统被屏蔽。

---

## 一、接口定义

在 Delphi 中，我们定义了一个纯虚接口：

```pascal
type
  ICloudStorage = interface
    ['{GUID}']
    function UploadFile(LocalPath, RemotePath: string): Boolean;
    function DownloadFile(RemotePath, LocalPath: string): Boolean;
    function ListFiles(RemotePath: string): TArray<TFileInfo>;
    function DeleteFile(RemotePath: string): Boolean;
    function GetProviderName: string;
  end;
```

---

## 二、适配器实现

### 2.1 S3 Adapter
实现了 AWS S3 V4 签名算法。支持分块上传（Multipart Upload）。
适用于：AWS, MinIO, 阿里云 OSS, 腾讯云 COS。

### 2.2 WebDAV Adapter
实现了 WebDAV 的 `PROPFIND`, `PUT`, `GET` 方法。
需要解析复杂的 XML 响应。
适用于：Nextcloud, Synology NAS,堅果云。

### 2.3 Local Adapter
把本地文件夹当成云盘。
适用于：外部硬盘备份，或者调试。

---

## 三、工厂模式

`TCloudStorageFactory` 根据配置字符串（如 `s3://key:secret@endpoint/bucket`）自动创建对应的适配器实例。

```pascal
Storage := CloudFactory.CreateStorage('webdav://user:pass@192.168.1.100:5005');
Storage.UploadFile('c:\data.zip', '/backup/data.zip');
```

业务逻辑完全不需要关心这是 S3 还是 WebDAV。

---

## 四、总结

**抽象层是抵御变化的防波堤。**
通过 `ICloudStorage`，OmniSync 将 N 种云服务的差异收敛为一套标准接口。这不仅简化了开发，更让用户拥有了自由切换云厂商的权力。

---

*下一篇预告：《065-机器指纹密钥：无需用户设置密码的安全方案》*
