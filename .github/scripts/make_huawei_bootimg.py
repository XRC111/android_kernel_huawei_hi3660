"""
把未压缩的 ARM64 Image 打包成华为 Kirin960 可用的 boot.img
参考格式：ANDROID! boot.img，kernel 为 gzip 压缩，ramdisk_size=0（华为 kernel 分区设计）

用法:
    python make_huawei_bootimg.py <输入 Image> <输出 boot.img>

参数来源：分析 Kirin960_HM2_Kernel_KPM.img（他人可刷镜像）得到
  - page_size   = 2048
  - kernel_addr = 0x00080000
  - ramdisk_addr= 0x07c00000
  - tags_addr   = 0x07a00000
  - second_addr = 0x00f00000
  - ramdisk_size= 0（无 ramdisk）
"""
import sys, struct, os, gzip, io

# ==== boot.img header 参数（Kirin960 华为格式）====
MAGIC = b'ANDROID!'
KERNEL_ADDR = 0x00080000
RAMDISK_ADDR = 0x07C00000
SECOND_ADDR = 0x00F00000
TAGS_ADDR = 0x07A00000
PAGE_SIZE = 2048
CMDLINE = (
    b'loglevel=4 initcall_debug=n page_tracker=on slub_min_objects=16 '
    b'unmovable_isolate1=2:192M,3:224M,4:256M printktimer=0xfff0a000,0'
)


def align(v, a):
    return (v + a - 1) // a * a


def build_bootimg(kernel_gz, dtb=None, out_path='boot.img'):
    """
    boot_img_hdr (AOSP v0/v1, 老格式，华为 Kirin960 用这个):
      0x00 magic[8]
      0x08 kernel_size
      0x0c kernel_addr
      0x10 ramdisk_size
      0x14 ramdisk_addr
      0x18 second_size
      0x1c second_addr
      0x20 tags_addr
      0x24 page_size
      0x28 dtb_size        (v1+)
      0x2c unused / header_version
      0x30 os_version (v1+)
      0x34 name[16]
      0x44 cmdline[512]
      0x244 id[32]
      0x264 extra_cmdline[1024]
    """
    hdr_size = PAGE_SIZE  # header 占一页
    kernel_size = len(kernel_gz)
    dtb_size = len(dtb) if dtb else 0

    h = bytearray(hdr_size)
    h[0:8] = MAGIC
    struct.pack_into('<I', h, 0x08, kernel_size)
    struct.pack_into('<I', h, 0x0C, KERNEL_ADDR)
    struct.pack_into('<I', h, 0x10, 0)             # ramdisk_size = 0
    struct.pack_into('<I', h, 0x14, RAMDISK_ADDR)
    struct.pack_into('<I', h, 0x18, 0)             # second_size = 0
    struct.pack_into('<I', h, 0x1C, SECOND_ADDR)
    struct.pack_into('<I', h, 0x20, TAGS_ADDR)
    struct.pack_into('<I', h, 0x24, PAGE_SIZE)
    struct.pack_into('<I', h, 0x28, 1)             # dtb_size = 1 (Huawei 习惯占位)
    struct.pack_into('<I', h, 0x2C, 0x1200000A)  # header_version (Huawei magic value)
    struct.pack_into('<I', h, 0x30, 0)             # os_version
    h[0x34:0x44] = b'logl\x00'.ljust(16, b'\x00')
    h[0x44:0x44 + len(CMDLINE)] = CMDLINE

    # 组装：header + kernel(页对齐) + dtb(页对齐)
    # 重要：必须用带 header 的 h（新建全 0 数组会丢 ANDROID! magic）
    out = h
    out += kernel_gz
    out += b'\x00' * (align(len(kernel_gz), PAGE_SIZE) - len(kernel_gz))
    if dtb:
        out += dtb
        out += b'\x00' * (align(len(dtb), PAGE_SIZE) - len(dtb))

    with open(out_path, 'wb') as f:
        f.write(out)
    return len(out)


def gzip_kernel(image_path, level=9):
    """gzip 压缩内核（bootloader 负责解压）"""
    data = open(image_path, 'rb').read()
    buf = io.BytesIO()
    # mtime=0 保证可复现
    with gzip.GzipFile(fileobj=buf, mode='wb', compresslevel=level, mtime=0) as gz:
        gz.write(data)
    return buf.getvalue()


def main():
    if len(sys.argv) < 3:
        print('用法: python make_huawei_bootimg.py <输入Image> <输出boot.img> [dtb文件]')
        sys.exit(1)

    src, dst = sys.argv[1], sys.argv[2]
    dtb_path = sys.argv[3] if len(sys.argv) > 3 else None

    raw = os.path.getsize(src)
    print('输入 Image: %d bytes (%.2f MB)' % (raw, raw / 1024 / 1024))

    print('gzip 压缩中 (level 9)...')
    gz = gzip_kernel(src)
    print('压缩后: %d bytes (%.2f MB)  压缩比 %.1f%%' %
          (len(gz), len(gz) / 1024 / 1024, len(gz) / raw * 100))

    dtb = open(dtb_path, 'rb').read() if dtb_path and os.path.exists(dtb_path) else None
    if dtb:
        print('附加 DTB: %d bytes' % len(dtb))

    size = build_bootimg(gz, dtb, dst)
    print()
    print('=== 生成完成 ===')
    print('输出: %s' % dst)
    print('大小: %d bytes (%.2f MB)' % (size, size / 1024 / 1024))
    print()
    print('刷入命令:')
    print('  adb reboot bootloader')
    print('  fastboot flash kernel %s' % os.path.basename(dst))
    print('  fastboot reboot')


if __name__ == '__main__':
    main()
