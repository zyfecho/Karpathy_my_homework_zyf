---
title: "SPI通信"
date: 2026-04-28
tags: ["通信协议", "SPI", "外设"]
sources: ["八股默写.docx", "index.md"]
---

# SPI 通信

SPI（Serial Peripheral Interface）是一种全双工、同步、串行通信协议，支持多主机多从机结构，速度比 [[i2c]] 更快。

## 信号线

| 信号 | 说明 |
|------|------|
| MOSI | Master Out Slave In — 主机输出，从机接收 |
| MISO | Master In Slave Out — 主机接收，从机输出 |
| SCL/SCLK | 时钟信号，由主机产生，用于同步 |
| CS/SS | 片选信号，低电平有效，选择从设备 |

## 特点

- **全双工**：MOSI和MISO同时工作，可同时收发
- **同步通信**：由SCL时钟线同步
- **多从机**：每个从机一根CS线，主机通过拉低对应CS选择通信对象
- **速度快**：相比I2C，SPI没有地址开销和ACK机制，吞吐量更高
- **线数多**：至少4根线（MOSI/MISO/SCL/CS），从机越多CS线越多

## HAL库函数

```c
// 阻塞方式
HAL_SPI_Transmit(&hspi, pData, Size, Timeout);
HAL_SPI_Receive(&hspi, pData, Size, Timeout);
HAL_SPI_TransmitReceive(&hspi, pTxData, pRxData, Size, Timeout);

// 中断方式
HAL_SPI_Transmit_IT(&hspi, pData, Size);
HAL_SPI_Receive_IT(&hspi, pData, Size);
HAL_SPI_TransmitReceive_IT(&hspi, pTxData, pRxData, Size);

// DMA方式
HAL_SPI_Transmit_DMA(&hspi, pData, Size);
HAL_SPI_Receive_DMA(&hspi, pData, Size);
HAL_SPI_TransmitReceive_DMA(&hspi, pTxData, pRxData, Size);
```

## 回调函数

```c
HAL_SPI_TxCpltCallback(&hspi);       // 发送完成
HAL_SPI_RxCpltCallback(&hspi);       // 接收完成
HAL_SPI_TxRxCpltCallback(&hspi);     // 同时收发完成
```

## 相关主题

- [[i2c]] — 另一种同步串行协议，线数少但速度较低
- [[uart]] — 异步串行通信
- [[hal-quick-reference]] — 完整HAL函数速查
- [[interview-guide]] — 面试常考SPI与I2C对比

## 来源

- `八股默写.docx` — SPI协议要点：MOSI/MISO/SCL/CS、全双工同步
- `index.md` — HAL库SPI函数速查
