---
title: "I2C通信"
date: 2026-04-28
tags: ["通信协议", "I2C", "外设", "OLED"]
sources: ["实验07_GUI应用实验(V25).pdf", "八股默写.docx", "index.md"]
---

# I2C 通信

I2C（IIC）是由飞利浦公司开发的两线式同步串行总线协议，半双工，一主多从结构。使用SCL（时钟线）和SDA（数据线）两根线。

## 协议要点

### 信号定义

- **起始信号**：SCL高电平期间，SDA从高拉低
- **停止信号**：SCL高电平期间，SDA从低拉高
- **数据有效**：SCL高时读取SDA（SDA不可跳变）；SCL低时写入SDA（SDA可跳变）

### 通信流程

1. 主机发送起始信号
2. 发送7位从设备地址 + 1位读/写方向位
3. 等待从设备ACK应答
4. 传输数据，每字节后需ACK应答
5. 主机发送停止信号

### 关键特性

- **开漏输出 + 上拉电阻**：I2C引脚采用开漏模式，总线空闲时由上拉电阻保持高电平
- **ACK应答**：接收方在每字节后拉低SDA表示确认
- **重复起始**：不发停止信号直接发新的起始信号，用于读寄存器等复合操作
- 相比 [[spi]] 速度较低，但只需两根线

## 硬件I2C vs 软件模拟I2C

| 方式 | 说明 |
|------|------|
| 硬件I2C | 使用MCU的I2C外设和专用引脚，效率高，代码简单，调用控制函数即可 |
| 软件模拟I2C | 用任意GPIO模拟时序，更灵活，不受引脚限制，移植方便，低速场景更常用 |

## OLED显示屏驱动（I2C应用）

- 常见0.96寸单色OLED，分辨率128×64，驱动IC为SSD1306
- 通信方式：I2C或SPI
- 驱动文件中需注意 `SSD1306_i2c.c` 中的引脚宏定义是否与实际接线一致

## HAL库函数

```c
// 阻塞方式
HAL_I2C_Master_Transmit(&hi2c, DevAddr, pData, Size, Timeout);
HAL_I2C_Master_Receive(&hi2c, DevAddr, pData, Size, Timeout);

// 中断方式
HAL_I2C_Master_Transmit_IT(&hi2c, DevAddr, pData, Size);
HAL_I2C_Master_Receive_IT(&hi2c, DevAddr, pData, Size);

// DMA方式
HAL_I2C_Master_Transmit_DMA(&hi2c, DevAddr, pData, Size);
HAL_I2C_Master_Receive_DMA(&hi2c, DevAddr, pData, Size);
```

## 相关主题

- [[gpio]] — I2C使用开漏输出+上拉配置
- [[spi]] — 另一种同步串行协议，速度更快
- [[uart]] — 异步串行通信
- [[hal-quick-reference]] — 完整HAL函数速查
- [[sensors-and-modules]] — OLED模块I2C驱动
- [[interview-guide]] — 面试常考I2C协议细节

## 来源

- `实验07_GUI应用实验(V25).pdf` — I2C总线原理、硬件/软件I2C对比、OLED驱动实验（32页）
- `八股默写.docx` — I2C协议要点：开漏+上拉、ACK、重复起始、读寄存器流程
- `index.md` — HAL库I2C函数速查
