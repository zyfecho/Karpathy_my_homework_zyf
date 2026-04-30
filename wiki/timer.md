---
title: "定时器"
date: 2026-04-28
tags: ["STM32", "定时器", "PWM", "外设"]
sources: ["实验08_STM32定时器应用实验(V25).pdf", "自选实验2-1_ 乐曲播放实验(V25).pdf", "第八章 定时器V3.pptx", "index.md"]
---

# 定时器

STM32定时器是对周期脉冲信号的计数单元，通常对外设时钟信号进行计数。使用时需关注三点：位宽、计数值和计数溢出操作。

## 核心概念

- **时钟频率**：传递给定时器的周期性时钟信号频率
- **计数时钟 CK_CNT**：经预分频后的实际计数时钟
- **预分频系数 PSC**：`fCK_CNT = fTIM_CLK / (PSC + 1)`
- **自动重装载值 ARR**：计数达到 ARR 时产生溢出
- **定时周期公式**：`T = (ARR + 1) * (PSC + 1) / fTIM_CLK`

### 计算示例

168MHz 时钟下实现 100ms 定时：
- PSC = 16800 - 1，ARR = 1000 - 1
- T = 1000 × 16800 / 168000000 = 0.1s

> 注意：PSC 范围 0~65535，16位定时器 ARR 范围 0~65535，32位定时器 ARR 范围 0~4294967295。

## STM32F407 定时器分类

| 名称 | 分类 | 位数 | 计数模式 | 捕获/比较通道 | 互补输出 | 默认时钟 |
|------|------|------|----------|--------------|---------|---------|
| TIM1、TIM8 | 高级定时器 | 16 | 上/下/双向 | 4 | 有 | 168MHz |
| TIM2、TIM5 | 通用定时器 | 32 | 上/下/双向 | 4 | 无 | 84MHz |
| TIM3、TIM4 | 通用定时器 | 16 | 上/下/双向 | 4 | 无 | 84MHz |
| TIM6、TIM7 | 基本定时器 | 16 | 上/下/双向 | 0 | 无 | 84MHz |
| TIM9 | 通用定时器 | 16 | 向上 | 2 | 无 | 168MHz |
| TIM10~14 | 通用定时器 | 16 | 向上 | 1 | 无 | 84/168MHz |

- TIM1/TIM8 互补输出常用于**电机控制**
- TIM2/TIM5 为32位，可用于**测量高频信号频率**

## PWM 输出

PWM 信号三要素：
1. **频率** — 控制音调（如蜂鸣器）或电机转速
2. **占空比** — 控制功率/音量（典型值50%）
3. **脉冲持续个数** — 控制时长

PWM 硬件输出相比软件模拟翻转IO的优势：控制维度更全面、CPU无需持续干预、波形更平滑。

## HAL库常用函数

```c
HAL_TIM_Base_Start_IT(&htim);           // 启动定时器（中断方式）
HAL_TIM_PWM_Start(&htim, channel);      // 启动PWM输出
HAL_TIM_IC_Start(&htim, channel);       // 启动输入捕获
HAL_TIM_Encoder_Start(&htim, channels); // 启动编码器模式
```

## 回调函数

```c
HAL_TIM_PeriodElapsedCallback(&htim);       // 周期溢出回调
HAL_TIM_IC_CaptureCallback(&htim);          // 输入捕获回调
HAL_TIM_PWM_PulseFinishedCallback(&htim);   // PWM脉冲完成回调
```

## 相关主题

- [[clock-system-rcc]] — 定时器时钟来源
- [[hal-quick-reference]] — 完整HAL函数速查
- [[sensors-and-modules]] — 蜂鸣器PWM控制、步进电机脉冲控制
- [[freertos-basics]] — RTOS中的软件定时器

## 来源

- `实验08_STM32定时器应用实验(V25).pdf` — 定时器基本概念、分类、定时周期计算与CubeMX配置（22页）
- `自选实验2-1_乐曲播放实验(V25).pdf` — PWM控制蜂鸣器播放MIDI音乐（19页）
- `第八章 定时器V3.pptx` — 定时器课件
- `index.md` — HAL库定时器函数速查
