---
title: "FreeRTOS任务管理"
date: 2026-04-28
tags: ["FreeRTOS", "任务管理", "CMSIS"]
sources: ["实验04_RTOS任务管理实验(V25).pdf", "任务调度方式与任务状态.docx"]
---

# FreeRTOS 任务管理

FreeRTOS 提供完整的任务生命周期管理，包括创建、挂起、恢复、删除和优先级调整。CMSIS v2 对原版 FreeRTOS 函数进行了封装。

## 任务管理函数

| 功能 | FreeRTOS 原版 | CMSIS v2 封装 | 说明 |
|------|--------------|---------------|------|
| 创建任务 | xTaskCreate | osThreadNew | 创建任务并加入活动任务列表 |
| 获取任务名 | pcTaskGetName | osThreadGetName | 获取任务名称 |
| 获取当前任务 | xTaskGetCurrentTaskHandle | osThreadGetId | 返回当前运行任务ID |
| 获取任务状态 | xTaskGetSchedulerState | osThreadGetState | 获取任务当前状态 |
| 设置优先级 | vTaskPrioritySet | osThreadSetPriority | 更改任务优先级 |
| 获取优先级 | uxTaskPriorityGet | osThreadGetPriority | 获取任务优先级 |
| 挂起任务 | vTaskSuspend | osThreadSuspend | 暂停任务，保持阻塞状态 |
| 恢复任务 | vTaskResume | osThreadResume | 恢复被挂起的任务 |
| 退出当前任务 | vTaskDelete | osThreadExit | 终止当前任务 |
| 让出CPU | portYIELD | osThreadYield | 交给下一个就绪态线程 |
| 终止任务 | vTaskDelete | osThreadTerminate | 终止指定任务 |
| 获取栈空间 | uxTaskGetStackHighWaterMark | osThreadGetStackSpace | 获取可用堆栈空间 |

## 挂起 vs 终止

- **osThreadSuspend**：挂起任务，保持阻塞状态，可用 osThreadResume 恢复
  - 如果恢复的任务优先级高于当前任务，系统会立即切换到该任务
- **osThreadTerminate**：终止任务后只能用 osThreadNew 重新创建
  - 新任务的内部变量值无法恢复到终止时的状态

> 要暂停后恢复任务，应使用 Suspend/Resume，而不是 Terminate + New。

## 任务通知（线程标志）

每个 FreeRTOS 任务有一个32位通知值，可用于简单的任务间通信和同步：

| 功能 | CMSIS v2 函数 | 说明 |
|------|--------------|------|
| 设置标志 | osThreadFlagsSet | 设置指定任务的标志 |
| 清除标志 | osThreadFlagsClear | 清除当前任务的标志 |
| 获取标志 | osThreadFlagsGet | 获取当前任务的标志 |
| 等待标志 | osThreadFlagsWait | 等待一个或多个标志位被设置 |

- 不需要额外创建通知变量，比消息队列更轻量
- 适合简单的任务间同步场景

## 任务调度

- 每个时刻只执行一个任务
- 优先级范围：硬件设置（CubeMX）时为 0-31，软件设置时可自定义
- 新任务创建后放入就绪列表

## 相关主题

- [[freertos-basics]] — FreeRTOS 基础概念与裸机对比
- [[freertos-ipc]] — 消息队列、信号量等更复杂的通信方式
- [[timer]] — 定时器与任务调度的配合

## 来源

- `实验04_RTOS任务管理实验(V25).pdf` — 任务管理函数详解、挂起/恢复/终止对比、任务通知机制（17页）
- `任务调度方式与任务状态.docx` — 任务调度方式与优先级范围总结
