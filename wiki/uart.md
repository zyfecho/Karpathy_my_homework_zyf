---
title: "UART串口通信"
date: 2026-04-28
tags: ["通信协议", "UART", "RS232", "RS485"]
sources: ["实验06_基于RTOS的串口通信实验(V25).pdf", "八股默写.docx", "第九章 串口通信V2.pptx", "index.md"]
---

# UART 串口通信

UART（Universal Asynchronous Receiver/Transmitter）是嵌入式系统中最常用的异步串行通信接口，全双工，使用TX和RX两根线。

## 串行通信基本参数

1. **波特率** — 每秒传输的数据位数（bps），如4800bps = 600 byte/s
2. **数据位** — 5/6/7/8位，从最低有效位开始传输
3. **起始位** — 逻辑"0"，标志一帧数据开始
4. **停止位** — 可以是1位、1.5位或2位
5. **奇偶校验位** — 有限差错校验，通信双方需约定一致

## 电平标准对比

| 协议 | 双工 | 电平 | 特点 |
|------|------|------|------|
| UART (TTL) | 全双工 | 3.3V/5V | 最基本的串口通信 |
| RS232 | 全双工 | +5~+12V为低，-12~-5V为高 | 负逻辑电平，需MAX232转换芯片 |
| RS485 | 半双工 | 差分信号 | 双线电平差确定信号，抑制共模干扰，适合远距离多机通信 |

## USB虚拟串口

现代开发板通常使用USB转串口方案：
- 开发板上的STM32F103C8T6实现DAP调试下载器 + USB虚拟串口
- 将STM32F4的串口1虚拟为Windows可识别的USB串口
- Win10以上系统可自动识别，Win7/8需另装驱动

## HAL库函数

```c
// 阻塞方式
HAL_UART_Transmit(&huart, pData, Size, Timeout);
HAL_UART_Receive(&huart, pData, Size, Timeout);

// 中断方式
HAL_UART_Transmit_IT(&huart, pData, Size);
HAL_UART_Receive_IT(&huart, pData, Size);

// DMA方式
HAL_UART_Transmit_DMA(&huart, pData, Size);
HAL_UART_Receive_DMA(&huart, pData, Size);
```

## 回调函数

```c
HAL_UART_TxCpltCallback(&huart);                    // 发送完成
HAL_UART_RxCpltCallback(&huart);                    // 接收完成
HAL_UARTEx_RxEventCallback(&huart, Size);           // 接收事件（如IDLE触发）
```

## 相关主题

- [[i2c]] — 同步串行通信协议
- [[spi]] — 同步串行通信协议
- [[hal-quick-reference]] — 完整HAL函数速查
- [[freertos-ipc]] — RTOS下的串口通信设计
- [[sensors-and-modules]] — ESP01模块通过串口AT指令通信
- [[interview-guide]] — 面试常考通信协议对比

## 来源

- `实验06_基于RTOS的串口通信实验(V25).pdf` — 串口通信原理、USB虚拟串口、基于RTOS的串口实验（28页）
- `八股默写.docx` — UART/RS232/RS485电气特性对比
- `第九章 串口通信V2.pptx` — 串口通信课件
- `index.md` — HAL库UART函数速查
