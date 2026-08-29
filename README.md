Kirin 960 Pangu Kernel (H9) + KernelSU / SUSFS
===

Based on Pangu 9.1 EROFS kernel (H9 branch), with KernelSU + SUSFS integrated,
and the kernel base ported from Linux 4.9.148 to 4.9.194 (Google ACK `gregkh/linux-4.9.y`).

基于 Pangu 9.1 EROFS 内核（H9 分支），叠加 KernelSU + SUSFS，内核基线由 4.9.148 移植至 4.9.194。

Supported devices / 支持机型
---

**H9 branch / H9 分支** — for these Kirin 960 devices:

- Honor 9 (荣耀 9, STF)
- Honor V9 / Honor 8 Pro (荣耀 V9, DUKE)
- Huawei Nova 2S
- Huawei Mate 9 series
- Huawei MediaPad M5 (平板 M5)
- Other Kirin960 / Kirin960s devices

**NOT for Huawei P10 series (VTR).** P10 uses a different WiFi driver that is not
interchangeable with other hi3660 devices. This tree's defconfig
(`Pangu_Kirin960_defconfig`) contains **zero VTR (P10) options** — it is STF + DUKE only.

**不支持华为 P10 系列（VTR）**：P10 的 WiFi 驱动与其他 hi3660 机型不通用；
本仓库 defconfig 中不含任何 VTR 配置项（仅 STF 荣耀9 + DUKE 荣耀V9）。

Supports EMUI 9.0 / 9.1 (including EROFS filesystem) and ROMs based on them,
as well as HarmonyOS 2.0. Note: EMUI 9.0 and 9.1 use different versions.

支持 EMUI 9.0 / 9.1（含 EROFS）及基于其的 ROM，同时支持 HarmonyOS 2.0。
注意 EMUI 9.0 与 9.1 使用不同版本。

Kernel version / 内核版本
---

- Linux **4.9.194** — ported from 4.9.148 to the ACK 4.9.194 baseline
- Target: continue porting up to **4.9.337** (143 version segments / 9721 commits, in progress)

Features / 特性
---

Inherited from Pangu (原版特性):

- Unlock selinux limitation
- Unblock the hidden CPU governor Schedutil and GPU governor GPU SCENE AWARE
- Port Blu_Schedutil governor from [Honor 9 EMUI8 Proto Kernel](http://github.com/JBolho/Proto) and set as default
- Add Dynamic Stune Boost
- Add WireGuard
- Port ZEN governor and set as default
- Port JPEG Processing Engine from Kirin 970
- fsync on/off support
- Support Spectrum kernel tuning APP
- EROFS filesystem support

Added in this repository (本仓库新增):

- **KernelSU** — kernel-level root solution
- **SUSFS v1.5.5** — deep hiding (sus_path / sus_mount / sus_kstat / try_umount /
  spoof uname / open redirect / spoof cmdline-or-bootconfig)
- **Linux 4.9.194** security and driver updates from upstream ACK

Build / 编译
---

Automated by GitHub Actions (ubuntu-22.04 + `gcc-aarch64-linux-gnu`, GCC 11):

- defconfig: `Pangu_Kirin960_defconfig`
- Output: `arch/arm64/boot/Image` — **DTB is NOT included**

Any push to the `ack-test` branch triggers a build; the image is published as the
`kernel-image` artifact on the Actions run page.

Install / 刷入
---

1. Download `Image` from Releases (or from the Actions artifact) and rename it to `kernel.img`
2. Extract the **DTB** (device tree) and ramdisk from your device's **stock boot.img**
3. Repack **this kernel Image + your stock DTB + your stock ramdisk** into a new boot.img
   (magiskboot / mkbootimg)
4. `fastboot flash boot boot.img`

⚠️ The DTB determines final device matching — always use the stock DTB of your own model.
⚠️ Flashing is risky. Make sure you can recover your device before proceeding.

⚠️ DTB 决定最终机型匹配，务必使用你自己机型的原厂 DTB。刷机有风险，请确认具备救砖能力。

Credits
===

[ **kindle4jerry** ](http://github.com/kindle4jerry)

[ **JBolho** ](http://github.com/JBolho)

[ **engstk** ](https://github.com/engstk)

[ **joshuous** ](http://github.com/joshuous/)

[ **KernelSU** — tiann ](https://github.com/tiann/KernelSU)

[ **SUSFS for KernelSU** — simonpunk ](https://gitlab.com/simonpunk/susfs4ksu)

And many testers
