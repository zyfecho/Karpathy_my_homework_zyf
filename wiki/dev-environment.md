---
title: "开发环境搭建"
date: 2026-04-28
tags: ["Keil", "CubeMX", "开发环境", "STM32"]
sources: ["STM32开发工具下载Keil和CubeMX.docx", "KEIL中参考手册和数据手册的查找.docx", "第三章 STM32微控制器开发环境的搭建V4.pptx", "第四章 STM32CubeMX软件的使用V3.pptx", "第五章 MDK-ARM软件的使用V2.pptx"]
---

# 开发环境搭建

STM32开发需要两个核心工具：Keil MDK（编译调试）和 STM32CubeMX（图形化配置与代码生成）。两者安装的固件库功能不同，互为补充。

## Keil MDK 安装

1. 运行 `MDK.exe`，一路 Next 完成安装
2. 激活：以管理员身份运行 `keygen.exe`，打开 FILE → License Management，复制 CID 到 keygen，Target 选 ARM，生成密钥后粘贴到 LIC 栏，点击 ADD LIC
3. 安装固件库：双击 `KEIL.STM32F1XX_DFP.2.4.0.pack`（或对应芯片型号的包）
4. 安装编辑器插件（详见视频教程）

### 调试器识别问题

魔术棒 → Debug → Settings，如果 SWDIO 处未识别到设备，需安装 `WCH-LinkUtility/Drv_Link/` 下的驱动。安装后可在设备管理器中确认。

## STM32CubeMX 安装

1. 双击 `setupcubemx.exe` 安装
2. 打开后点击 HELP → Manage embedded software packages
3. 如遇报错，在任务管理器中结束 OPENJDK 进程后重试
4. 选择所需的 STM32F1/F4 等固件包，点击 INSTALL
5. 如提示登录，需要 ST 官网账号

## 两种固件库的区别

| 固件库 | 用途 |
|--------|------|
| Keil MDK 固件库 | **芯片支持包**，让编译器识别芯片的内存地址、外设地址等底层信息，用于编译和调试 |
| CubeMX 固件库 | **硬件抽象层库（HAL）+ 示例代码**，通过库函数操作芯片外设，无需直接操作寄存器 |

## 参考视频

- Keil5和STM32CubeMX安装：[BV16GWEz8EfK](https://www.bilibili.com/video/BV16GWEz8EfK)
- Keil固件库下载：[BV1VC4y1k7iC](https://www.bilibili.com/video/BV1VC4y1k7iC)

## 相关主题

- [[stm32-overview]] — STM32产品概述
- [[clock-system-rcc]] — CubeMX中RCC时钟配置
- [[dev-tools-ai]] — AI辅助开发工具

## 来源

- `STM32开发工具下载Keil和CubeMX.docx` — Keil与CubeMX完整安装流程及固件库区别说明
- `KEIL中参考手册和数据手册的查找.docx` — Keil中查阅技术文档的方法
- `第三章 STM32微控制器开发环境的搭建V4.pptx` — 开发环境搭建课件
- `第四章 STM32CubeMX软件的使用V3.pptx` — CubeMX使用课件
- `第五章 MDK-ARM软件的使用V2.pptx` — MDK-ARM使用课件
