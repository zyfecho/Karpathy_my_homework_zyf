---
title: "HAL库函数速查"
date: 2026-04-28
tags: ["STM32", "HAL", "API参考"]
sources: ["index.md"]
---

# HAL 库函数速查

STM32 HAL（Hardware Abstraction Layer）库提供统一的外设操作接口。大多数外设支持三种工作方式：阻塞（Polling）、中断（IT）和 DMA。

## GPIO

```c
HAL_GPIO_WritePin(端口, 引脚号, 电平状态);   // 写引脚电平
HAL_GPIO_ReadPin(端口, 引脚号);             // 读引脚电平
HAL_GPIO_TogglePin(端口, 引脚号);           // 翻转引脚电平
```

## UART

```c
HAL_UART_Transmit(&huart, pData, Size, Timeout);       // 发送（阻塞）
HAL_UART_Receive(&huart, pData, Size, Timeout);        // 接收（阻塞）
HAL_UART_Transmit_IT(&huart, pData, Size);             // 发送（中断）
HAL_UART_Receive_IT(&huart, pData, Size);              // 接收（中断）
HAL_UART_Transmit_DMA(&huart, pData, Size);            // 发送（DMA）
HAL_UART_Receive_DMA(&huart, pData, Size);             // 接收（DMA）
```

## I2C

```c
HAL_I2C_Master_Transmit(&hi2c, DevAddr, pData, Size, Timeout);    // 主机发送（阻塞）
HAL_I2C_Master_Receive(&hi2c, DevAddr, pData, Size, Timeout);     // 主机接收（阻塞）
HAL_I2C_Master_Transmit_IT(&hi2c, DevAddr, pData, Size);          // 主机发送（中断）
HAL_I2C_Master_Receive_IT(&hi2c, DevAddr, pData, Size);           // 主机接收（中断）
HAL_I2C_Master_Transmit_DMA(&hi2c, DevAddr, pData, Size);         // 主机发送（DMA）
HAL_I2C_Master_Receive_DMA(&hi2c, DevAddr, pData, Size);          // 主机接收（DMA）
```

## SPI

```c
HAL_SPI_Transmit(&hspi, pData, Size, Timeout);                         // 发送（阻塞）
HAL_SPI_Receive(&hspi, pData, Size, Timeout);                          // 接收（阻塞）
HAL_SPI_TransmitReceive(&hspi, pTxData, pRxData, Size, Timeout);      // 同时收发（阻塞）
HAL_SPI_Transmit_IT(&hspi, pData, Size);                               // 发送（中断）
HAL_SPI_Receive_IT(&hspi, pData, Size);                                // 接收（中断）
HAL_SPI_TransmitReceive_IT(&hspi, pTxData, pRxData, Size);            // 同时收发（中断）
HAL_SPI_Transmit_DMA(&hspi, pData, Size);                              // 发送（DMA）
HAL_SPI_Receive_DMA(&hspi, pData, Size);                               // 接收（DMA）
HAL_SPI_TransmitReceive_DMA(&hspi, pTxData, pRxData, Size);           // 同时收发（DMA）
```

## 定时器

```c
HAL_TIM_Base_Start(&htim);                     // 启动基本定时器
HAL_TIM_Base_Start_IT(&htim);                  // 启动基本定时器（中断）
HAL_TIM_PWM_Start(&htim, Channel);             // 启动PWM输出
HAL_TIM_IC_Start(&htim, Channel);              // 启动输入捕获
HAL_TIM_Encoder_Start(&htim, Channels);        // 启动编码器模式
```

## ADC

```c
HAL_ADC_Start(&hadc);                          // 启动ADC（阻塞）
HAL_ADC_Start_IT(&hadc);                       // 启动ADC（中断）
HAL_ADC_Start_DMA(&hadc, pData, Length);       // 启动ADC（DMA）
HAL_ADC_PollForConversion(&hadc, Timeout);     // 等待转换完成
HAL_ADC_GetValue(&hadc);                       // 获取采样值
```

## 中断/事件回调函数

```c
HAL_GPIO_EXTI_Callback(GPIO_Pin);                          // GPIO外部中断
HAL_UART_TxCpltCallback(&huart);                           // UART发送完成
HAL_UART_RxCpltCallback(&huart);                           // UART接收完成
HAL_UARTEx_RxEventCallback(&huart, Size);                  // UART接收事件（IDLE）
HAL_I2C_MasterTxCpltCallback(&hi2c);                       // I2C主机发送完成
HAL_I2C_MasterRxCpltCallback(&hi2c);                       // I2C主机接收完成
HAL_SPI_TxCpltCallback(&hspi);                             // SPI发送完成
HAL_SPI_RxCpltCallback(&hspi);                             // SPI接收完成
HAL_SPI_TxRxCpltCallback(&hspi);                           // SPI收发完成
HAL_ADC_ConvCpltCallback(&hadc);                           // ADC转换完成
HAL_TIM_PeriodElapsedCallback(&htim);                      // 定时器周期溢出
HAL_TIM_IC_CaptureCallback(&htim);                         // 输入捕获完成
HAL_TIM_PWM_PulseFinishedCallback(&htim);                  // PWM脉冲完成
```

## 相关主题

- [[gpio]] | [[uart]] | [[i2c]] | [[spi]] | [[timer]] — 各外设详细说明

## 来源

- `index.md` — HAL库函数速查手册原始文件
