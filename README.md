<div align="center">

# Pangu Kernel · Kirin 960（HarmonyOS）

**华为 Kirin 960 设备的内核源码（Pangu 分支），支持 EMUI 9 / HarmonyOS 2.0**

[![Platform](https://img.shields.io/badge/SoC-Kirin%20960-0078D4?style=flat-square)](#适用机型)
[![Kernel](https://img.shields.io/badge/Kernel-4.9-orange?style=flat-square)](#)
[![License](https://img.shields.io/badge/License-GPL--2.0-blue?style=flat-square)](./COPYING)

</div>

---

> **仓库说明**：本仓库是 Kirin 960 内核源码的 fork，在上游 Pangu 内核基础上补充 HarmonyOS 2.0 与 EROFS 支持。
> 中文说明与刷机包见 [Gitee: Pangu9.1EROFS](https://gitee.com/maimaiguanfan/Pangu9.1EROFS)。

## 特性

- 解除 SELinux 限制
- 解锁隐藏的 CPU governor `Schedutil` 与 GPU governor `GPU SCENE AWARE`
- 移植 `Blu_Schedutil`（来自 Honor 9 EMUI8 Proto Kernel）并设为默认
- 动态 Stune Boost
- WireGuard 支持
- 移植 `ZEN` governor 并设为默认（可选切回）
- 从 Kirin 970 移植 JPEG 处理引擎
- fsync 开关
- 支持 Spectrum 内核调校 App

## 适用机型

| 版本 | 机型 |
| --- | --- |
| **P10** | 华为 P10 系列 |
| **H9** | 荣耀 9、荣耀 8 Pro（V9）、Nova 2S、Mate 9 系列、平板 M5（含 Kirin 960s 设备） |

兼容性：

- 支持全部 EMUI 9 版本及基于其的 ROM，包括 EROFS 文件系统
- 支持 HarmonyOS 2.0
- EMUI 9.0 与 9.1 使用不同版本，请勿混刷

## 构建

本仓库是完整内核源码树，需要华为 Kirin 960 对应的交叉编译工具链（aarch64-linux-android）。

```bash
export ARCH=arm64
export CROSS_COMPILE=aarch64-linux-android-

# 选择对应机型的 defconfig（以仓库内 arch/arm64/configs 为准）
make ARCH=arm64 <defconfig>
make ARCH=arm64 -j$(nproc)
```

产物：`arch/arm64/boot/Image.gz-dtb`

> 不同 ROM 分支的 defconfig 名称不同；刷入前请确认与当前系统版本（EMUI 9.0 / 9.1 / HarmonyOS 2.0）匹配。

## 刷入说明

1. 解锁 Bootloader（会导致数据清空与保修失效）
2. 用对应机型的工具打包 `boot.img`（含内核 + ramdisk）
3. `fastboot flash boot boot.img`

> ⚠️ **风险自负**：刷内核可能导致无法开机、数据丢失或硬件损坏。请先完整备份，并确认机型与系统版本完全匹配。

## 致谢

- [kindle4jerry](https://github.com/kindle4jerry)
- [JBolho](https://github.com/JBolho) — Blu_Schedutil
- [engstk](https://github.com/engstk) — ZEN governor
- [joshuous](https://github.com/joshuous)
- 以及所有参与测试的机友

## License

GPL-2.0（见 [COPYING](./COPYING)）。内核源码遵循上游 Linux 内核许可；分发修改版时请同样开源。
